#!/usr/bin/env python3
"""Aplica os arquivos corrigidos sobre uma cópia existente do repositório.

Uso: python INSTALAR_NO_REPO.py "C:\\caminho\\labcore"
Preserva static/assets (PNGs originais), .venv, .git e db.sqlite3; faz backup.
"""
from __future__ import annotations

import shutil
import sys
from datetime import datetime
from pathlib import Path

SOURCE = Path(__file__).resolve().parent
KEEP_DIRS = {'.venv', '.git', '__pycache__', 'staticfiles', 'node_modules'}
KEEP_NAMES = {'db.sqlite3', 'INSTALAR_NO_REPO.py'}


def install(target: Path) -> int:
    target = target.expanduser().resolve()
    if not target.is_dir() or not (target / 'main.py').is_file():
        print('ERRO: informe a pasta ORIGINAL do repositório labcore (onde existe main.py).')
        return 1
    if target == SOURCE:
        print('Os arquivos já estão na pasta de destino. Não há cópia a realizar.')
        print('Confirme a presença das imagens em static/assets e execute INICIAR_LABCORE.bat.')
        return 0
    files = []
    for file in SOURCE.rglob('*'):
        if not file.is_file():
            continue
        rel = file.relative_to(SOURCE)
        if any(component in KEEP_DIRS for component in rel.parts):
            continue
        if file.name in KEEP_NAMES or rel.parts[:2] == ('static', 'assets') and file.suffix.lower() == '.png':
            continue
        files.append((file, target / rel))
    backup = target / ('backup_labcore_' + datetime.now().strftime('%Y%m%d_%H%M%S_%f'))
    for source, dest in files:
        if dest.is_file():
            original = backup / dest.relative_to(target)
            original.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(dest, original)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, dest)
    old_pngs = len(list((target / 'static' / 'assets').glob('*.png')))
    print(f'OK: {len(files)} arquivos atualizados em {target}')
    print(f'Backup dos arquivos anteriores: {backup}')
    print(f'Capturas PNG originais preservadas: {old_pngs}')
    if old_pngs < 30:
        print('ATENÇÃO: a pasta static/assets ainda precisa das imagens originais do GitHub.')
    print('Agora execute INICIAR_LABCORE.bat na pasta do repositório.')
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Uso: python INSTALAR_NO_REPO.py "C:\\Users\\...\\labcore"')
        raise SystemExit(2)
    raise SystemExit(install(Path(sys.argv[1])))
