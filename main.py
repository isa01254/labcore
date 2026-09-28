#!/usr/bin/env python3
"""Execute `python main.py` para preparar e abrir o LabCore no navegador."""

import os
import sys
import threading
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "labcore_web.settings")


def usar_ambiente_virtual():
    """Evita que o VS Code use o Python global sem as dependências do projeto."""
    candidatos = (
        ROOT / ".venv" / "Scripts" / "python.exe",  # Windows
        ROOT / ".venv" / "bin" / "python",          # Linux/macOS
    )
    for python_venv in candidatos:
        if python_venv.is_file() and python_venv.resolve() != Path(sys.executable).resolve():
            os.execv(
                str(python_venv),
                [str(python_venv), str(ROOT / "main.py"), *sys.argv[1:]],
            )
            return


def main():
    usar_ambiente_virtual()
    try:
        from django.core.management import execute_from_command_line
    except ModuleNotFoundError as erro:
        print(f"Dependência ausente: {erro.name}")
        print("Instale usando o Python do ambiente virtual:")
        if os.name == "nt":
            print(r".\.venv\Scripts\python.exe -m pip install -r requirements.txt")
        else:
            print("python -m pip install -r requirements.txt")
        return 1

    if len(sys.argv) > 1:
        execute_from_command_line(["manage.py", *sys.argv[1:]])
        return 0

    # As imagens são parte do repositório original. Não bloquear o servidor
    # se o GitHub estiver fora do ar; o navegador apresenta fallback visual.
    from verificar_imagens import IMAGES, faltantes
    missing = faltantes()
    if missing:
        print(f"[LabCore] ATENÇÃO: faltam {len(missing)} de {len(IMAGES)} imagens originais.")
        print("[LabCore] Copie a pasta static/assets do seu repositório original.")
        print("[LabCore] O jogo abre mesmo assim, com imagens de reserva onde necessário.")
    else:
        print(f"[LabCore] {len(IMAGES)} imagens originais verificadas.")

    print("[LabCore] Preparando o banco de dados...")
    execute_from_command_line(["manage.py", "migrate", "--noinput"])

    print("[LabCore] Verificando o projeto...")
    execute_from_command_line(["manage.py", "check"])

    endereco = "http://127.0.0.1:8000/"
    print(f"[LabCore] Jogo disponível em {endereco}")
    print("[LabCore] Para encerrar, pressione Ctrl+C.")

    # Sem autoreload, não executa migrações duas vezes nem abre abas duplicadas.
    if os.environ.get("LABCORE_NO_BROWSER") != "1":
        abertura = threading.Timer(2.0, lambda: webbrowser.open(endereco))
        abertura.daemon = True
        abertura.start()

    execute_from_command_line(
        ["manage.py", "runserver", "127.0.0.1:8000", "--noreload"]
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
