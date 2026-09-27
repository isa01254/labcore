from django.contrib.auth.models import User
from django.db import models


class GameProgress(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="game_progress",
    )

    total_score = models.IntegerField(
        default=0
    )

    current_phase = models.IntegerField(
        default=1
    )

    unlocked_phases = models.JSONField(
        default=list
    )

    phase_scores = models.JSONField(
        default=dict
    )

    phase_stars = models.JSONField(
        default=dict
    )

    phase_times = models.JSONField(
        default=dict
    )

    correct_answers = models.IntegerField(
        default=0
    )

    mistakes = models.IntegerField(
        default=0
    )

    best_score = models.IntegerField(
        default=0
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def get_total_stars(self):
        """
        Soma todas as estrelas conquistadas
        nas fases.
        """

        if not isinstance(
            self.phase_stars,
            dict
        ):
            return 0

        total = 0

        for value in self.phase_stars.values():

            try:
                total += int(value)

            except (
                TypeError,
                ValueError
            ):
                continue

        return total

    def get_accuracy(self):
        """
        Retorna a porcentagem de acertos.
        """

        total_answers = (
            self.correct_answers
            + self.mistakes
        )

        if total_answers == 0:
            return 0

        return round(
            (
                self.correct_answers
                / total_answers
            ) * 100,
            2
        )

    def __str__(self):
        return (
            f"{self.user.username} "
            f"- {self.total_score} XP"
        )


class LeaderboardEntry(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="leaderboard_entries",
    )

    score = models.IntegerField(
        default=0
    )

    total_stars = models.IntegerField(
        default=0
    )

    accuracy = models.FloatField(
        default=0
    )

    completed_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = [
            "-score",
            "-total_stars",
            "-accuracy",
            "completed_at",
        ]

    def __str__(self):
        return (
            f"{self.user.username} "
            f"- {self.score} XP"
        )


class GameSession(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="game_sessions",
    )

    session_data = models.JSONField(
        default=dict
    )

    started_at = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=True
    )

    def __str__(self):
        status = (
            "ativa"
            if self.is_active
            else "encerrada"
        )

        return (
            f"{self.user.username} "
            f"- sessão {status}"
        )