"""Confere as capturas reais do GitHub sem internet e sem baixar arquivos na inicialização.

As PNG devem estar em `static/assets` do repositório original. Não são
substituídas por imagens fictícias; a interface tem desenhos de reserva
somente quando o arquivo original não estiver disponível.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'static' / 'assets'
IMAGES = tuple(
    f'Captura de tela 2026-08-31 {t}.png'
    for t in (
        '083042', '083055', '083109', '083119', '083151', '083158',
        '083215', '083221', '083238', '083246', '083255', '083306',
        '083311', '083318', '083324', '083334', '083340',
    )
) + tuple(
    f'Captura de tela 2026-09-21 {t}.png'
    for t in (
        '073857', '073906', '073911', '073915', '073919', '073925',
        '073938', '073950', '074100', '074107', '074113', '074127',
    )
) + ('Laboratório Sci-Fi Neon em Pixel Art.png',)
PNG_HEADER = b'\x89PNG\r\n\x1a\n'
PNG_END = b'\x00\x00\x00\x00IEND\xaeB`\x82'


def imagem_valida(filename: str, directory: Path = ASSETS) -> bool:
    file = directory / filename
    if not file.is_file() or file.stat().st_size < 2000:
        return False
    with file.open('rb') as handle:
        if handle.read(8) != PNG_HEADER:
            return False
        handle.seek(-12, 2)
        return handle.read(12) == PNG_END


def faltantes(directory: Path = ASSETS) -> list[str]:
    return [name for name in IMAGES if not imagem_valida(name, directory)]


if __name__ == '__main__':
    missing = faltantes()
    if not missing:
        print(f'OK: {len(IMAGES)} imagens originais válidas em {ASSETS}')
    else:
        print(f'Faltam ou estão corrompidas {len(missing)} das {len(IMAGES)} imagens:')
        for name in missing:
            print(' -', name)
        print('\nCopie static/assets do repositório original para esta pasta.')
    raise SystemExit(1 if missing else 0)
