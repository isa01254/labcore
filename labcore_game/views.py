"""Páginas, autenticação e persistência do jogo LabCore."""
import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_POST

from .models import GameProgress, LeaderboardEntry

PHASES = ((1, "Equipamentos"), (2, "Química"), (3, "Física"), (4, "Biologia"), (5, "Desafio final"))


def game_view(request):
    return render(request, "game.html")


def initial_progress(user):
    progress, _ = GameProgress.objects.get_or_create(
        user=user,
        defaults={"unlocked_phases": [1], "phase_scores": {}, "phase_stars": {}, "phase_times": {}},
    )
    return progress


def valid_int(value, maximum=10_000_000):
    # Não converte float para int; evita strings ou objetos malformados.
    if isinstance(value, bool):
        raise ValueError("Número inválido")
    if isinstance(value, int) or (isinstance(value, str) and value.isascii() and value.isdigit()):
        number = int(value)
        if 0 <= number <= maximum:
            return number
    raise ValueError("Número fora do intervalo permitido")


def clean_phases(value):
    if not isinstance(value, list):
        raise ValueError("Lista de fases inválida")
    phases = {1}
    for item in value:
        phase = valid_int(item, 5)
        if phase < 1:
            raise ValueError("Fase inválida")
        phases.add(phase)
    return sorted(phases)


def clean_phase_dict(raw, *, star=False, time=False):
    if not isinstance(raw, dict):
        raise ValueError("Dados de fase inválidos")
    output = {}
    for key, value in raw.items():
        if not isinstance(key, str) or key not in ("1", "2", "3", "4", "5"):
            raise ValueError("Identificador de fase inválido")
        if star or time:
            output[key] = valid_int(value, 3 if star else 1_000_000)
        else:
            if not isinstance(value, (dict, int)) or isinstance(value, bool):
                raise ValueError("Pontuação por fase inválida")
            if isinstance(value, dict):
                if len(json.dumps(value, ensure_ascii=False)) > 4000:
                    raise ValueError("Dados de fase muito extensos")
                # O jogo mantém a relação de perguntas concluídas e pontos por fase.
                output[key] = value
            else:
                output[key] = valid_int(value)
    return output


@login_required
@require_POST
def save_progress(request):
    if len(request.body) > 30_000:
        return JsonResponse({"ok": False, "error": "Dados muito extensos."}, status=413)
    try:
        data = json.loads(request.body.decode("utf-8"))
        if not isinstance(data, dict):
            raise ValueError("O corpo deve ser um objeto JSON")
        total_score = valid_int(data.get("total_score", 0))
        current_phase = valid_int(data.get("current_phase", 1), 5)
        if current_phase < 1:
            raise ValueError("Fase inválida")
        unlocked = clean_phases(data.get("unlocked_phases", [1]))
        stars = clean_phase_dict(data.get("phase_stars", {}), star=True)
        times = clean_phase_dict(data.get("phase_times", {}), time=True)
        scores = clean_phase_dict(data.get("phase_scores", {}))
        correct = valid_int(data.get("correct_answers", 0))
        mistakes = valid_int(data.get("mistakes", 0))
        completed = data.get("game_completed") is True
        if current_phase not in unlocked:
            raise ValueError("A fase atual precisa estar desbloqueada")
        if completed and not all(stars.get(str(phase), 0) >= 1 for phase in range(1, 6)):
            raise ValueError("Conclua as cinco fases antes de registrar no ranking")
    except (ValueError, TypeError, UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({"ok": False, "error": "Progresso inválido. Confira os dados enviados."}, status=400)

    with transaction.atomic():
        progress = initial_progress(request.user)
        # O melhor resultado nunca diminui ao reiniciar o jogo.
        progress.best_score = max(progress.best_score, total_score)
        progress.total_score = total_score
        progress.current_phase = current_phase
        progress.unlocked_phases = unlocked
        progress.phase_scores = scores
        progress.phase_stars = stars
        progress.phase_times = times
        progress.correct_answers = correct
        progress.mistakes = mistakes
        progress.save()
        if completed:
            entry = LeaderboardEntry.objects.filter(user=request.user).order_by("-score").first()
            if entry is None:
                LeaderboardEntry.objects.create(
                    user=request.user, score=progress.best_score,
                    total_stars=progress.get_total_stars(), accuracy=progress.get_accuracy(),
                )
            elif progress.best_score >= entry.score:
                entry.score = progress.best_score
                entry.total_stars = progress.get_total_stars()
                entry.accuracy = progress.get_accuracy()
                entry.save(update_fields=["score", "total_stars", "accuracy"])
    return JsonResponse({"ok": True, "best_score": progress.best_score})


@login_required
@require_GET
def load_progress(request):
    progress = initial_progress(request.user)
    return JsonResponse({
        "ok": True,
        "total_score": progress.total_score,
        "current_phase": progress.current_phase,
        "unlocked_phases": progress.unlocked_phases,
        "phase_scores": progress.phase_scores,
        "phase_stars": progress.phase_stars,
        "phase_times": progress.phase_times,
        "correct_answers": progress.correct_answers,
        "mistakes": progress.mistakes,
        "best_score": progress.best_score,
    })


@require_GET
def leaderboard(request):
    # Uma linha por usuário, inclusive se a base antiga tiver duplicatas.
    entries = LeaderboardEntry.objects.select_related("user").order_by(
        "-score", "-total_stars", "-accuracy", "completed_at"
    )
    ranking, seen = [], set()
    for entry in entries:
        if entry.user_id in seen:
            continue
        seen.add(entry.user_id)
        ranking.append({
            "position": len(ranking) + 1,
            "username": entry.user.username,
            "score": entry.score,
            "total_stars": entry.total_stars,
            "accuracy": round(entry.accuracy, 2),
        })
        if len(ranking) == 20:
            break
    return JsonResponse({"ok": True, "leaderboard": ranking})


def register_view(request):
    if request.user.is_authenticated:
        return redirect("game")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        initial_progress(user)
        return redirect("game")
    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("game")
    error = None
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            initial_progress(user)
            return redirect("game")
        error = "Usuário ou senha incorretos."
    return render(request, "registration/login.html", {"error": error})


@login_required
@require_POST
def logout_view(request):
    logout(request)
    return redirect("game")


@login_required
@require_GET
def profile_view(request):
    return render(request, "profile.html", {"progress": initial_progress(request.user), "phases": PHASES})
