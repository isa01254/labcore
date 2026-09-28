from django.contrib import admin
from .models import GameProgress, GameSession, LeaderboardEntry


@admin.register(GameProgress)
class GameProgressAdmin(admin.ModelAdmin):
    list_display = ("user", "total_score", "best_score", "current_phase", "updated_at")
    search_fields = ("user__username",)
    list_select_related = ("user",)
    readonly_fields = ("updated_at",)


@admin.register(LeaderboardEntry)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ("user", "score", "total_stars", "accuracy", "completed_at")
    search_fields = ("user__username",)
    list_select_related = ("user",)


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ("user", "started_at", "is_active")
    search_fields = ("user__username",)
