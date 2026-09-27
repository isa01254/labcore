from django.contrib import admin

from .models import GameProgress, GameSession, LeaderboardEntry


@admin.register(GameProgress)
class GameProgressAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "total_score",
        "best_score",
        "current_phase",
        "total_stars_display",
        "accuracy_display",
        "updated_at",
    ]
    list_select_related = ["user"]
    search_fields = ["user__username"]
    ordering = ["-total_score"]
    readonly_fields = ["updated_at", "total_stars_display", "accuracy_display"]
    list_per_page = 25

    @admin.display(description="Estrelas")
    def total_stars_display(self, obj):
        return obj.get_total_stars()

    @admin.display(description="Precisao %")
    def accuracy_display(self, obj):
        return obj.get_accuracy()


@admin.register(LeaderboardEntry)
class LeaderboardEntryAdmin(admin.ModelAdmin):
    list_display = ["user", "score", "total_stars", "accuracy", "completed_at"]
    list_select_related = ["user"]
    search_fields = ["user__username"]
    list_filter = ["completed_at"]
    ordering = ["-score"]
    readonly_fields = ["completed_at"]
    list_per_page = 25


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ["user", "started_at", "is_active"]
    list_select_related = ["user"]
    list_filter = ["is_active", "started_at"]
    search_fields = ["user__username"]
    readonly_fields = ["started_at"]
    list_per_page = 25