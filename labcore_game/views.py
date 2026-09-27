import json

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.decorators.http import require_GET
from django.views.decorators.http import require_POST

from .models import GameProgress
from .models import LeaderboardEntry


def game_view(request):
    """
    Página principal do LabCore.
    """

    return render(
        request,
        "game.html",
    )


@login_required
@require_POST
def save_progress(request):
    """
    Salva o progresso atual do jogador.
    """

    try:
        data = json.loads(
            request.body.decode("utf-8")
        )

    except (
        json.JSONDecodeError,
        UnicodeDecodeError,
    ):
        return JsonResponse(
            {
                "ok": False,
                "error": "JSON inválido.",
            },
            status=400,
        )

    progress, created = (
        GameProgress.objects.get_or_create(
            user=request.user,
            defaults={
                "total_score": 0,
                "current_phase": 1,
                "unlocked_phases": [1],
                "phase_scores": {},
                "phase_stars": {},
                "phase_times": {},
                "correct_answers": 0,
                "mistakes": 0,
                "best_score": 0,
            },
        )
    )

    total_score = max(
        0,
        int(
            data.get(
                "total_score",
                progress.total_score,
            )
        ),
    )

    current_phase = max(
        1,
        int(
            data.get(
                "current_phase",
                progress.current_phase,
            )
        ),
    )

    unlocked_phases = data.get(
        "unlocked_phases",
        progress.unlocked_phases,
    )

    phase_scores = data.get(
        "phase_scores",
        progress.phase_scores,
    )

    phase_stars = data.get(
        "phase_stars",
        progress.phase_stars,
    )

    phase_times = data.get(
        "phase_times",
        progress.phase_times,
    )

    correct_answers = max(
        0,
        int(
            data.get(
                "correct_answers",
                progress.correct_answers,
            )
        ),
    )

    mistakes = max(
        0,
        int(
            data.get(
                "mistakes",
                progress.mistakes,
            )
        ),
    )

    if not isinstance(
        unlocked_phases,
        list,
    ):
        unlocked_phases = [1]

    if 1 not in unlocked_phases:
        unlocked_phases.insert(
            0,
            1,
        )

    unlocked_phases = sorted(
        set(
            int(phase)
            for phase in unlocked_phases
            if str(phase).isdigit()
        )
    )

    if not isinstance(
        phase_scores,
        dict,
    ):
        phase_scores = {}

    if not isinstance(
        phase_stars,
        dict,
    ):
        phase_stars = {}

    if not isinstance(
        phase_times,
        dict,
    ):
        phase_times = {}

    progress.total_score = (
        total_score
    )

    progress.current_phase = (
        current_phase
    )

    progress.unlocked_phases = (
        unlocked_phases
    )

    progress.phase_scores = (
        phase_scores
    )

    progress.phase_stars = (
        phase_stars
    )

    progress.phase_times = (
        phase_times
    )

    progress.correct_answers = (
        correct_answers
    )

    progress.mistakes = (
        mistakes
    )

    progress.best_score = max(
        progress.best_score,
        total_score,
    )

    progress.save()

    game_completed = bool(
        data.get(
            "game_completed",
            False,
        )
    )

    leaderboard_created = False

    if game_completed:

        accuracy = (
            progress.get_accuracy()
        )

        entry, created_entry = (
            LeaderboardEntry.objects.update_or_create(
                user=request.user,
                defaults={
                    "score": progress.total_score,
                    "total_stars": (
                        progress.get_total_stars()
                    ),
                    "accuracy": accuracy,
                },
            )
        )

        leaderboard_created = (
            created_entry
        )

    return JsonResponse(
        {
            "ok": True,
            "created": created,
            "leaderboard_created": (
                leaderboard_created
            ),
            "progress": {
                "total_score": (
                    progress.total_score
                ),
                "current_phase": (
                    progress.current_phase
                ),
                "unlocked_phases": (
                    progress.unlocked_phases
                ),
                "phase_scores": (
                    progress.phase_scores
                ),
                "phase_stars": (
                    progress.phase_stars
                ),
                "phase_times": (
                    progress.phase_times
                ),
                "correct_answers": (
                    progress.correct_answers
                ),
                "mistakes": (
                    progress.mistakes
                ),
                "best_score": (
                    progress.best_score
                ),
            },
        },
    )


@login_required
@require_GET
def load_progress(request):
    """
    Recupera o progresso salvo do jogador.
    """

    progress, created = (
        GameProgress.objects.get_or_create(
            user=request.user,
            defaults={
                "total_score": 0,
                "current_phase": 1,
                "unlocked_phases": [1],
                "phase_scores": {},
                "phase_stars": {},
                "phase_times": {},
                "correct_answers": 0,
                "mistakes": 0,
                "best_score": 0,
            },
        )
    )

    return JsonResponse(
        {
            "ok": True,
            "created": created,
            "total_score": (
                progress.total_score
            ),
            "current_phase": (
                progress.current_phase
            ),
            "unlocked_phases": (
                progress.unlocked_phases
            ),
            "phase_scores": (
                progress.phase_scores
            ),
            "phase_stars": (
                progress.phase_stars
            ),
            "phase_times": (
                progress.phase_times
            ),
            "correct_answers": (
                progress.correct_answers
            ),
            "mistakes": (
                progress.mistakes
            ),
            "best_score": (
                progress.best_score
            ),
        }
    )


@require_GET
def leaderboard(request):
    """
    Retorna os melhores jogadores.

    O ranking usa a melhor pontuação registrada
    de cada usuário.
    """

    entries = (
        LeaderboardEntry.objects
        .select_related("user")
        .order_by(
            "-score",
            "-total_stars",
            "-accuracy",
            "completed_at",
        )[:20]
    )

    ranking = []

    for position, entry in enumerate(
        entries,
        start=1,
    ):

        ranking.append(
            {
                "position": position,
                "username": (
                    entry.user.username
                ),
                "score": entry.score,
                "total_stars": (
                    entry.total_stars
                ),
                "accuracy": (
                    round(
                        entry.accuracy,
                        2,
                    )
                ),
            }
        )

    return JsonResponse(
        {
            "ok": True,
            "leaderboard": ranking,
        }
    )


def register_view(request):
    """
    Cadastro de novo jogador.
    """

    if request.user.is_authenticated:
        return redirect("game")

    if request.method == "POST":

        form = UserCreationForm(
            request.POST
        )

        if form.is_valid():

            user = form.save()

            login(
                request,
                user,
            )

            GameProgress.objects.get_or_create(
                user=user,
                defaults={
                    "unlocked_phases": [1],
                    "phase_scores": {},
                    "phase_stars": {},
                    "phase_times": {},
                },
            )

            return redirect("game")

    else:

        form = UserCreationForm()

    return render(
        request,
        "registration/register.html",
        {
            "form": form,
        },
    )


def login_view(request):
    """
    Login do jogador.
    """

    if request.user.is_authenticated:
        return redirect("game")

    error = None

    if request.method == "POST":

        username = (
            request.POST.get(
                "username",
                "",
            ).strip()
        )

        password = (
            request.POST.get(
                "password",
                "",
            )
        )

        user = authenticate(
            request,
            username=username,
            password=password,
        )

        if user is not None:

            login(
                request,
                user,
            )

            GameProgress.objects.get_or_create(
                user=user,
                defaults={
                    "unlocked_phases": [1],
                    "phase_scores": {},
                    "phase_stars": {},
                    "phase_times": {},
                },
            )

            return redirect("game")

        error = (
            "Usuário ou senha incorretos."
        )

    return render(
        request,
        "registration/login.html",
        {
            "error": error,
        },
    )


@login_required
@require_POST
def logout_view(request):
    """
    Encerra a sessão.
    """

    logout(request)

    return redirect("game")


@login_required
@require_GET
def profile_view(request):
    """
    Página do perfil do jogador.
    """

    progress = (
        GameProgress.objects
        .filter(
            user=request.user
        )
        .first()
    )

    if progress is None:

        progress = (
            GameProgress.objects.create(
                user=request.user,
                unlocked_phases=[1],
                phase_scores={},
                phase_stars={},
                phase_times={},
            )
        )

    phases = [
        (1, "Equipamentos"),
        (2, "Química"),
        (3, "Física"),
        (4, "Biologia"),
        (5, "Desafio Final"),
    ]

    return render(
        request,
        "profile.html",
        {
            "progress": progress,
            "phases": phases,
        },
    )