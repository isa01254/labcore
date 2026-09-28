#!/usr/bin/env python3
"""
LabCore - inicialização principal do jogo.

Uso:
    python main.py
    python main.py migrate
    python main.py createsuperuser
    python main.py check
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "labcore_web.settings")


def main() -> int:
    try:
        from django.core.management import execute_from_command_line
    except ModuleNotFoundError as exc:
        print(f"Dependência ausente: {exc.name}")
        print("Instale com:")
        print("python -m pip install -r requirements.txt")
        return 1

    args = sys.argv[1:]

    # Se o usuário digitou algum comando do Django, executa normalmente
    if args:
        execute_from_command_line(["manage.py", *args])
        return 0

    # Fluxo padrão: migrate -> check -> runserver
    print("[LabCore] Atualizando o banco de dados...")
    execute_from_command_line(["manage.py", "migrate", "--noinput"])

    print("[LabCore] Verificando o projeto...")
    execute_from_command_line(["manage.py", "check"])

    print("[LabCore] Iniciando o jogo...")
    print("Abra: http://127.0.0.1:8000")

    execute_from_command_line(["manage.py", "runserver", "127.0.0.1:8000"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())