from django.db import models
from django.contrib.auth.models import User


class GameProgress(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
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

        if isinstance(
            self.phase_stars,
            dict
        ):
            return sum(
                self.phase_stars.values()
            )

        return 0


class LeaderboardEntry(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    score = models.IntegerField()

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
        ordering = ['-score']


class GameSession(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
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