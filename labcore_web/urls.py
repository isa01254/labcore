from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from labcore_game import views


urlpatterns = [
    path(
        'admin/',
        admin.site.urls
    ),

    path(
        '',
        views.game_view,
        name='game'
    ),

    path(
        'api/save/',
        views.save_progress,
        name='save_progress'
    ),

    path(
        'api/load/',
        views.load_progress,
        name='load_progress'
    ),

    path(
        'api/leaderboard/',
        views.leaderboard,
        name='leaderboard'
    ),

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'profile/',
        views.profile_view,
        name='profile'
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        document_root=settings.STATIC_ROOT
    )