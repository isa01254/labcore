#!/usr/bin/env python
"""
Ponto de entrada unico do LabCore.

Uso:
    python main.py                    # aplica migracoes e sobe o servidor
    python main.py migrate            # so aplicas migracoes
    python main.py createsuperuser
    python main.py collectstatic
    python main.py <qualquer comando do django>
"""

import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "labcore_web.settings")

# Comandos que valem a pena rodar sozinhos antes do runserver.
PRE_RUN = ("migrate",)


def main() -> int:
    try:
        import django
        from django.core.management import execute_from_command_line
    except ModuleNotFoundError as exc:
        print("")
        print("ERRO: dependencia faltando ->", exc.name)
        print("")
        print("Rode:")
        print("    python -m pip install -r requirements.txt")
        print("")
        return 1

    django.setup()

    argv = sys.argv[1:]

    if not argv:
        argv = list(PRE_RUN) + ["runserver", "0.0.0.0:8000"]
    elif argv[0] == "runserver" and "0.0.0.0:8000" not in argv:
        argv.append("0.0.0.0:8000")

    execute_from_command_line(["manage.py", *argv])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())