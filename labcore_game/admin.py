from django.contrib import admin
from .models import GameProgress, LeaderboardEntry
@admin.register(GameProgress)
class GPAdmin(admin.ModelAdmin): list_display=['user','total_score','current_phase','best_score']
@admin.register(LeaderboardEntry)
class LBAdmin(admin.ModelAdmin): list_display=['user','score','total_stars','accuracy']