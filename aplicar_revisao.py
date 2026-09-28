
#!/usr/bin/env python3

"""
Aplica a revisão do LabCore aos arquivos originais.

Requisitos:
- main.py atualizado
- static/labcore_review.css
- static/labcore_review.js
- projeto original do GitHub
"""

import re
import shutil
import sys

from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent

GAME = ROOT / "templates" / "game.html"
VIEWS = ROOT / "labcore_game" / "views.py"

CSS = ROOT / "static" / "labcore_review.css"
JS = ROOT / "static" / "labcore_review.js"


def substituir(texto, antigo, novo, nome):
    quantidade = texto.count(antigo)

    if quantidade != 1:
        raise ValueError(
            f"{nome}: esperado um trecho, "
            f"encontrados {quantidade}. "
            "Confira a versão do arquivo."
        )

    return texto.replace(antigo, novo, 1)


def revisar_game(texto):

    if "labcore_review.js" in texto:
        raise ValueError(
            "A revisão já está instalada no game.html."
        )

    # Corrigir o nome da imagem de fundo.

    texto = substituir(
        texto,
        "Laborat#U00f3rio Sci-Fi Neon em Pixel Art.png",
        "Laboratório Sci-Fi Neon em Pixel Art.png",
        "Imagem de fundo"
    )

    # Corrigir o botão de saída para POST.

    texto = substituir(
        texto,
        '''            <a
                href="/logout/"
                class="header-button"
            >
                SAIR
            </a>''',
        '''            <form class="header-logout"
                  method="post"
                  action="/logout/">
                {% csrf_token %}
                <button type="submit"
                        class="header-button">
                    SAIR
                </button>
            </form>''',
        "Botão de saída"
    )

    # Permitir que visitantes visualizem sua pontuação.

    texto = substituir(
        texto,
        '''        {% else %}

            <a
                href="/login/"''',
        '''        {% else %}

            <span id="headerScore" hidden>0</span>

            <a
                href="/login/"''',
        "Pontuação de visitantes"
    )

    # Carregar o CSS.

    texto = substituir(
        texto,
        "</head>",
        '''    <link rel="stylesheet"
          href="{% static 'labcore_review.css' %}">
</head>''',
        "Estilos do jogo"
    )

    # Usar armazenamento individual por conta.

    texto, quantidade = re.subn(
        r'(localStorage\.(?:setItem|getItem)\(\s*)"labcore"',
        r'\1window.LABCORE_STORAGE_KEY',
        texto
    )

    if quantidade != 2:
        raise ValueError(
            "Não encontrei as duas operações "
            "originais de armazenamento local."
        )

    # Configuração das imagens e do jogador.

    configuracao = '''<script>
window.LABCORE_ASSET_BASE = "{% static 'assets/' %}";
window.LABCORE_AUTHENTICATED = {% if user.is_authenticated %}true{% else %}false{% endif %};
window.LABCORE_STORAGE_KEY = "labcore_{{ user.pk|default:'guest' }}";
window.LABCORE_SESSION_STARTED = false;
</script>

<script>


/* ================================================================
   DESAFIOS'''

    texto = substituir(
        texto,
        '''<script>


/* ================================================================
   DESAFIOS''',
        configuracao,
        "Configuração do JavaScript"
    )

    # Carregar o script após o código original.

    texto = substituir(
        texto,
        '''</script>


</body>''',
        '''</script>

<script src="{% static 'labcore_review.js' %}"></script>


</body>''',
        "Integração do JavaScript"
    )

    return texto


def revisar_views(texto):

    if "Corpo da requisição deve ser um objeto JSON." in texto:
        raise ValueError(
            "A revisão já está instalada no views.py."
        )

    marcador = (
        "    progress, created = (\n"
        "        GameProgress.objects.get_or_create("
    )

    if texto.count(marcador) != 2:
        raise ValueError(
            "Não encontrei as rotinas originais "
            "de salvamento e carregamento."
        )

    # Validar o formato dos dados enviados.

    validacao = (
        "    if not isinstance(data, dict):\n"
        "        return JsonResponse(\n"
        '            {"ok": False, "error": '
        '"Corpo da requisição deve ser um objeto JSON."},\n'
        "            status=400,\n"
        "        )\n\n"
    )

    texto = texto.replace(
        marcador,
        validacao + marcador,
        1
    )

    # Tratar números inválidos.

    inicio = texto.find(
        "    total_score = max(\n"
    )

    fim = texto.find(
        "    if not isinstance(\n"
        "        unlocked_phases,\n"
        "        list,\n"
        "    ):",
        inicio
    )

    if inicio < 0 or fim < 0:
        raise ValueError(
            "Não encontrei os campos numéricos "
            "do progresso."
        )

    trecho = texto[inicio:fim]

    protegido = (
        "    try:\n"
        + "".join(
            "    " + linha if linha.strip() else linha
            for linha in trecho.splitlines(keepends=True)
        )
        + "    except (TypeError, ValueError, OverflowError):\n"
        '        return JsonResponse(\n'
        '            {"ok": False, '
        '"error": "Dados numéricos inválidos."},\n'
        '            status=400,\n'
        '        )\n\n'
    )

    texto = (
        texto[:inicio] +
        protegido +
        texto[fim:]
    )

    # Impedir números de fase inválidos.

    texto = substituir(
        texto,
        "            if str(phase).isdigit()\n",
        "            if len(str(phase)) <= 2 "
        "and str(phase).isascii() "
        "and str(phase).isdigit()\n",
        "Validação das fases"
    )

    texto = substituir(
        texto,
        '''    progress.current_phase = (
        current_phase
    )''',
        "    progress.current_phase = min(5, current_phase)",
        "Fase atual"
    )

    texto = substituir(
        texto,
        '''    progress.unlocked_phases = (
        unlocked_phases
    )''',
        "    progress.unlocked_phases = "
        "[phase for phase in unlocked_phases "
        "if 1 <= phase <= 5]",
        "Fases desbloqueadas"
    )

    # Verificar a conclusão das cinco fases.

    texto = substituir(
        texto,
        '''    game_completed = bool(
        data.get(
            "game_completed",
            False,
        )
    )''',
        '''    game_completed = (
        data.get("game_completed") is True
        and progress.current_phase == 5
        and all(
            str(phase) in progress.phase_stars
            for phase in range(1, 6)
        )
    )''',
        "Conclusão do jogo"
    )

    # Salvar o recorde no ranking.

    texto = substituir(
        texto,
        '                    "score": progress.total_score,',
        '                    "score": progress.best_score,',
        "Recorde no ranking"
    )

    return texto


def main():

    arquivos = [
        GAME,
        VIEWS,
        CSS,
        JS,
        ROOT / "main.py"
    ]

    faltando = [
        str(arquivo)
        for arquivo in arquivos
        if not arquivo.is_file()
    ]

    if faltando:
        raise FileNotFoundError(
            "Arquivos não encontrados:\n" +
            "\n".join(faltando)
        )

    # Prepara todas as alterações antes de gravar.

    novo_game = revisar_game(
        GAME.read_text(encoding="utf-8")
    )

    novo_views = revisar_views(
        VIEWS.read_text(encoding="utf-8")
    )

    # Backup.

    backup = ROOT / (
        "labcore_backup_" +
        datetime.now().strftime("%Y%m%d_%H%M%S")
    )

    backup.mkdir(
        parents=True,
        exist_ok=False
    )

    for arquivo in [GAME, VIEWS]:
        destino = backup / arquivo.relative_to(ROOT)

        destino.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        shutil.copy2(arquivo, destino)

    # Instalação.

    GAME.write_text(
        novo_game,
        encoding="utf-8"
    )

    VIEWS.write_text(
        novo_views,
        encoding="utf-8"
    )

    print()
    print("LabCore revisado com sucesso!")
    print("Backup:", backup.name)
    print()
    print("Para jogar, execute:")
    print("python main.py")
    print()
    print("Acesse: http://127.0.0.1:8000")


if __name__ == "__main__":
    try:
        main()

    except (
        ValueError,
        FileNotFoundError,
        FileExistsError,
        OSError
    ) as erro:
        print(
            "Revisão não aplicada:",
            erro,
            file=sys.stderr
        )

        raise SystemExit(1)
