import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import GameProgress, LeaderboardEntry

PHASES = [
    (1, "Equipamentos"),
    (2, "Quimica"),
    (3, "Fisica"),
    (4, "Biologia"),
    (5, "Final"),
]

MAX_PHASE = len(PHASES)


def _as_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _as_dict(value):
    return value if isinstance(value, dict) else {}


def _as_phase_list(value):
    if not isinstance(value, list):
        return [1]
    out = []
    for item in value:
        n = _as_int(item, 0)
        if 1 <= n <= MAX_PHASE and n not in out:
            out.append(n)
    return out or [1]


def _payload(request):
    """Le o JSON do POST sem estourar 500 em corpo invalido."""
    try:
        data = json.loads(request.body or b"{}")
    except (ValueError, UnicodeDecodeError):
        return None
    return data if isinstance(data, dict) else None


def game_view(request):
    return render(request, "game.html")


@csrf_exempt
@require_http_methods(["POST"])
def save_progress(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "login"}, status=401)

    data = _payload(request)
    if data is None:
        return JsonResponse({"error": "invalid_json"}, status=400)

    total_score = max(0, _as_int(data.get("total_score"), 0))
    current_phase = max(1, min(MAX_PHASE, _as_int(data.get("current_phase"), 1)))
    unlocked = _as_phase_list(data.get("unlocked_phases"))
    phase_stars = _as_dict(data.get("phase_stars"))
    phase_scores = _as_dict(data.get("phase_scores"))
    phase_times = _as_dict(data.get("phase_times"))
    correct = max(0, _as_int(data.get("correct_answers"), 0))
    mistakes = max(0, _as_int(data.get("mistakes"), 0))

    with transaction.atomic():
        progress, _ = GameProgress.objects.get_or_create(
            user=request.user,
            defaults={"unlocked_phases": [1]},
        )

        progress.total_score = total_score
        progress.current_phase = current_phase
        progress.unlocked_phases = unlocked
        progress.phase_stars = phase_stars
        progress.phase_scores = phase_scores
        progress.phase_times = phase_times
        progress.correct_answers = correct
        progress.mistakes = mistakes
        progress.best_score = max(progress.best_score, total_score)
        progress.save()

        stars = progress.get_total_stars()

        if data.get("game_completed"):
            LeaderboardEntry.objects.create(
                user=request.user,
                score=progress.total_score,
                total_stars=stars,
                accuracy=progress.get_accuracy(),
            )

    return JsonResponse({"ok": True, "total_stars": stars, "best_score": progress.best_score})


@require_http_methods(["GET"])
def load_progress(request):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "login"}, status=401)

    empty = {
        "total_score": 0,
        "current_phase": 1,
        "unlocked_phases": [1],
        "phase_stars": {},
        "phase_scores": {},
        "phase_times": {},
        "correct_answers": 0,
        "mistakes": 0,
        "best_score": 0,
    }

    progress = GameProgress.objects.filter(user=request.user).first()
    if progress is None:
        return JsonResponse(empty)

    return JsonResponse(
        {
            "total_score": progress.total_score,
            "current_phase": progress.current_phase,
            "unlocked_phases": progress.unlocked_phases,
            "phase_stars": progress.phase_stars,
            "phase_scores": progress.phase_scores,
            "phase_times": progress.phase_times,
            "correct_answers": progress.correct_answers,
            "mistakes": progress.mistakes,
            "best_score": progress.best_score,
        }
    )


@require_http_methods(["GET"])
def leaderboard(request):
    entries = LeaderboardEntry.objects.select_related("user")[:20]
    return JsonResponse(
        {
            "leaderboard": [
                {
                    "username": e.user.username,
                    "score": e.score,
                    "total_stars": e.total_stars,
                    "accuracy": e.accuracy,
                }
                for e in entries
            ]
        }
    )


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("game")
        messages.error(request, "Confira os campos do formulario.")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = (request.POST.get("username") or "").strip()
        password = request.POST.get("password") or ""
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.POST.get("next") or "game")
        messages.error(request, "Usuario ou senha invalidos.")
    return render(request, "registration/login.html")


@require_http_methods(["GET", "POST"])
def logout_view(request):
    logout(request)
    return redirect("game")


@login_required
def profile_view(request):
    progress = GameProgress.objects.filter(user=request.user).first()
    return render(request, "profile.html", {"progress": progress, "phases": PHASES})