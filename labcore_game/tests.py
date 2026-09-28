"""Testes de integração executados por `python main.py test`."""
import json
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import GameProgress, LeaderboardEntry


class LabCoreTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="cientista", password="SenhaSegura123!4")

    def test_home_e_ranking_publicos(self):
        self.assertEqual(self.client.get(reverse("game")).status_code, 200)
        self.assertEqual(self.client.get(reverse("leaderboard")).json()["leaderboard"], [])

    def test_progresso_requer_login(self):
        self.assertEqual(self.client.get(reverse("load_progress")).status_code, 302)

    def test_salvar_carregar_e_registrar_ranking(self):
        self.client.force_login(self.user)
        payload = {
            "total_score": 650, "current_phase": 5,
            "unlocked_phases": [1, 2, 3, 4, 5],
            "phase_scores": {"1": {"score": 150, "done": ["microscope"], "claimed": ["microscope"], "bonus": 50}},
            "phase_stars": {str(i): 1 for i in range(1, 6)},
            "phase_times": {"1": 55},
            "correct_answers": 6, "mistakes": 1, "game_completed": True,
        }
        response = self.client.post(reverse("save_progress"), data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200, response.content)
        self.assertTrue(response.json()["ok"])
        self.assertEqual(GameProgress.objects.get(user=self.user).total_score, 650)
        self.assertEqual(self.client.get(reverse("load_progress")).json()["current_phase"], 5)
        self.assertEqual(LeaderboardEntry.objects.filter(user=self.user).count(), 1)
        self.assertEqual(self.client.get(reverse("leaderboard")).json()["leaderboard"][0]["score"], 650)
        payload["total_score"] = 400
        response = self.client.post(reverse("save_progress"), data=json.dumps(payload), content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(LeaderboardEntry.objects.get(user=self.user).score, 650)

    def test_recusa_pontuacao_invalida_e_conclusao_falsa(self):
        self.client.force_login(self.user)
        for data in ('not json', '[]', '{"total_score": "abc"}'):
            response = self.client.post(reverse("save_progress"), data=data, content_type="application/json")
            self.assertEqual(response.status_code, 400)
        incomplete = {
            "total_score": 100, "current_phase": 1, "unlocked_phases": [1],
            "game_completed": True, "phase_stars": {"1": 1}
        }
        response = self.client.post(reverse("save_progress"), data=json.dumps(incomplete), content_type="application/json")
        self.assertEqual(response.status_code, 400)

    def test_logout_por_post(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.assertEqual(self.client.post(reverse("logout")).status_code, 302)
