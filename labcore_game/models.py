"""Modelos compatíveis com a base de dados do LabCore original."""
from django.conf import settings
from django.db import models


class GameProgress(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="game_progress")
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

    def get_total_stars(self):
        return sum(
            max(0, min(3, int(value)))
            for value in (self.phase_stars or {}).values()
            if str(value).isdigit()
        )

    def get_accuracy(self):
        attempts = self.correct_answers + self.mistakes
        return round(100 * self.correct_answers / attempts, 2) if attempts else 0.0

    def __str__(self):
        return f"{self.user.username}: {self.total_score} XP"


class LeaderboardEntry(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="leaderboard_entries")
    score = models.IntegerField(default=0)
    total_stars = models.IntegerField(default=0)
    accuracy = models.FloatField(default=0)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-score", "-total_stars", "-accuracy", "completed_at"]

    def __str__(self):
        return f"{self.user.username}: {self.score} XP"


class GameSession(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="game_sessions")
    session_data = models.JSONField(default=dict)
    started_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}: sessão {'ativa' if self.is_active else 'encerrada'}"
