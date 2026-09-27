from django.conf import settings
from django.db import models


class GameProgress(models.Model):
    """Progresso salvo de cada usuario no jogo."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="game_progress",
    )

    total_score = models.IntegerField(default=0)
    current_phase = models.IntegerField(default=1)
    unlocked_phases = models.JSONField(default=list)
    phase_scores = models.JSONField(default=dict)
    phase_stars = models.JSONField(default=dict)
    phase_times = models.JSONField(default=dict)
    correct_answers = models.IntegerField(default=0)
    mistakes = models.IntegerField(default=0)
    best_score = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Progresso do jogo"
        verbose_name_plural = "Progressos do jogo"

    def __str__(self):
        return f"Progresso de {self.user}"

    def get_total_stars(self):
        if isinstance(self.phase_stars, dict):
            return sum(
                v for v in self.phase_stars.values() if isinstance(v, (int, float))
            )
        return 0

    def get_accuracy(self):
        total = self.correct_answers + self.mistakes
        if total <= 0:
            return 0.0
        return round(self.correct_answers / total * 100, 2)


class LeaderboardEntry(models.Model):
    """Uma linha do ranking, criada a cada fim de partida."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="leaderboard_entries",
    )

    score = models.IntegerField(db_index=True)
    total_stars = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Entrada do ranking"
        verbose_name_plural = "Ranking"
        ordering = ["-score", "-total_stars", "completed_at"]

    def __str__(self):
        return f"{self.user} - {self.score} pts"


class GameSession(models.Model):
    """Sessao de jogo (historico/retomada)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="game_sessions",
    )

    session_data = models.JSONField(default=dict)
    started_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Sessao de jogo"
        verbose_name_plural = "Sessoes de jogo"
        ordering = ["-started_at"]

    def __str__(self):
        return f"Sessao de {self.user} ({self.started_at:%d/%m/%Y %H:%M})"