# Esquema inicial compatível com o LabCore original.
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name="GameProgress", fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("total_score", models.IntegerField(default=0)),
                ("current_phase", models.IntegerField(default=1)),
                ("unlocked_phases", models.JSONField(default=list)),
                ("phase_scores", models.JSONField(default=dict)),
                ("phase_stars", models.JSONField(default=dict)),
                ("phase_times", models.JSONField(default=dict)),
                ("correct_answers", models.IntegerField(default=0)),
                ("mistakes", models.IntegerField(default=0)),
                ("best_score", models.IntegerField(default=0)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="game_progress", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="GameSession", fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("session_data", models.JSONField(default=dict)),
                ("started_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.BooleanField(default=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="game_sessions", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="LeaderboardEntry", fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("score", models.IntegerField(default=0)),
                ("total_stars", models.IntegerField(default=0)),
                ("accuracy", models.FloatField(default=0)),
                ("completed_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="leaderboard_entries", to=settings.AUTH_USER_MODEL)),
            ], options={"ordering": ["-score", "-total_stars", "-accuracy", "completed_at"]},
        ),
    ]
