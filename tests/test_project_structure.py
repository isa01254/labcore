"""Testes offline, independentes de Django e da rede."""
import ast
import re
import unittest
from pathlib import Path

from verificar_imagens import IMAGES

ROOT = Path(__file__).resolve().parents[1]


class ProjectTests(unittest.TestCase):
    def test_files(self):
        expected = [
            'main.py', 'manage.py', 'requirements.txt', 'verificar_imagens.py',
            'INICIAR_LABCORE.bat', 'INSTALAR_NO_REPO.py',
            'labcore_game/models.py', 'labcore_game/views.py', 'labcore_game/tests.py',
            'labcore_game/migrations/0001_initial.py', 'labcore_web/settings.py',
            'labcore_web/urls.py', 'templates/game.html', 'templates/profile.html',
            'templates/registration/login.html', 'templates/registration/register.html',
            'static/labcore.js', 'static/labcore.css', 'static/assets/balanca.svg',
        ]
        self.assertFalse([name for name in expected if not (ROOT / name).is_file()])

    def test_python_syntax(self):
        for file in ROOT.rglob('*.py'):
            if '.venv' not in file.parts:
                ast.parse(file.read_text('utf-8'), filename=str(file))

    def test_screens_and_image_references(self):
        js = (ROOT / 'static/labcore.js').read_text('utf-8')
        html = (ROOT / 'templates/game.html').read_text('utf-8')
        found = {f'Captura de tela 2026-08-31 {v}.png' for v in re.findall(r'aug\("(\d+)"\)', js)}
        found.update(f'Captura de tela 2026-09-21 {v}.png' for v in re.findall(r'sep\("(\d+)"\)', js))
        found.update(re.findall(r'assets/([^\']+\.png)', html))
        self.assertTrue(found.issubset(set(IMAGES)))
        self.assertEqual(len(IMAGES), 30)
        self.assertIn('img: "balanca.svg"', js)
        for element in ('playButton', 'phaseCards', 'answerButtons', 'touchControls', 'questionImage', 'assetWarning'):
            self.assertIn(f'id="{element}"', html)

    def test_no_whitenoise_or_mandatory_download(self):
        settings = (ROOT / 'labcore_web/settings.py').read_text('utf-8')
        main = (ROOT / 'main.py').read_text('utf-8')
        self.assertNotIn('WhiteNoiseMiddleware', settings)
        self.assertNotIn('prepare_images', main)
        self.assertIn('execute_from_command_line', main)


if __name__ == '__main__':
    unittest.main()
