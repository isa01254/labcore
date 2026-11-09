
#!/usr/bin/env python3
"""
LABCORE - INSTALADOR DA EXPANSAO PARA 8 FASES

Execute em uma pasta separada do projeto original.
Mantenha na mesma pasta deste script:
- labcore-expansao.js
- labcore-expansao.css

Exemplo:
py -3 aplicar_expansao.py --verificar "C:\\Projetos\\labcore"
py -3 aplicar_expansao.py "C:\\Projetos\\labcore"
"""

from __future__ import annotations

import argparse
import datetime
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def replace_exact(content, old, new, label, expected=1):
    count = content.count(old)

    if count != expected:
        raise RuntimeError(
            f"Versão incompatível em {label}. "
            f"Trecho encontrado {count} vez(es); esperado: {expected}. "
            "Nenhum arquivo foi modificado."
        )

    return content.replace(old, new)


# =========================================================
# 1. ATUALIZAR JAVASCRIPT ORIGINAL
# =========================================================

def patch_javascript(source):
    label = "static/labcore.js"

    rules = [
        (
            "    // Arte adicional do mapa,",
            '    // Carregar expansão das fases.\n'
            '    if (typeof window.LabCoreExpansao === "function") '
            'window.LabCoreExpansao(phases);\n'
            '    const TOTAL_PHASES = Object.keys(phases).length;\n'
            '    // Arte adicional do mapa,',
            1
        ),
        (
            "n >= 1 && n <= 5",
            "n >= 1 && n <= TOTAL_PHASES",
            1
        ),
        (
            "integer(raw.phase, 1, 5)",
            "integer(raw.phase, 1, TOTAL_PHASES)",
            1
        ),
        (
            "for (let phase = 1; phase <= 5; phase++)",
            "for (let phase = 1; phase <= TOTAL_PHASES; phase++)",
            2
        ),
        (
            "if (state.phase < 5) state.unlocked",
            "if (state.phase < TOTAL_PHASES) state.unlocked",
            1
        ),
        (
            "state.phase === 5 && [1, 2, 3, 4, 5].every(",
            "state.phase === TOTAL_PHASES && "
            "Array.from({length: TOTAL_PHASES}, "
            "(_, i) => i + 1).every(",
            1
        ),
        (
            'state.phase === 5 ? "Voltar ao mapa" : "Próxima fase"',
            'state.phase === TOTAL_PHASES ? "Voltar ao mapa" : "Próxima fase"',
            1
        ),
        (
            'if (state.phase === 5) showScreen("map");',
            'if (state.phase === TOTAL_PHASES) showScreen("map");',
            1
        ),
        (
            "conclua as cinco fases!",
            "conclua as oito fases!",
            1
        ),
        (
            "            button.append(image, name, starline, note);",
            '            const level = document.createElement("small");\n'
            '            level.className = "phase-level";\n'
            '            level.textContent = '
            '(phase.difficulty || "").split("—")[0].trim();\n'
            '            level.title = phase.difficulty || "";\n'
            '            button.append(image, name, starline, note, level);',
            1
        ),
        (
            '`${question.q} Resposta: ${question.options[question.correct]}.`',
            '`${question.q} Resposta: '
            '${question.type === "numeric" ? '
            '`${question.answer} ${question.unit || ""}` '
            ': question.options[question.correct]}.`',
            1
        ),
        (
            "if (index !== question.correct) {",
            'if (!(question.type === "numeric"\n'
            '            ? Number.isFinite(index) && '
            'Math.abs(index - question.answer) <= '
            '(question.tolerance ?? 0.01)\n'
            '            : index === question.correct)) {',
            1
        ),
        (
            "            button.disabled = true;\n"
            "            state.mistakes++;",
            '            if (question.type !== "numeric") '
            'button.disabled = true;\n'
            '            state.mistakes++;',
            1
        ),
        (
            "        if (newlyEarned) {\n"
            "            state.score += 100;",
            "        const points = question.points || "
            "(100 + (state.phase - 1) * 25);\n"
            "        if (newlyEarned) {\n"
            "            state.score += points;",
            1
        ),
        (
            "+ (newlyEarned ? 100 : 0)",
            "+ (newlyEarned ? points : 0)",
            1
        ),
        (
            '"Resposta correta! +100 XP"',
            '`Resposta correta! +${points} XP`',
            1
        ),
        (
            "const stars = errors >= 3 ? 1 : "
            "seconds <= 90 && errors === 0 ? 3 : 2;",
            "const parSeconds = phases[state.phase].parSeconds || 90;\n"
            "        const stars = errors >= 3 ? 1 : "
            "seconds <= parSeconds && errors === 0 ? 3 : 2;",
            1
        )
    ]

    for old, new, expected in rules:
        source = replace_exact(
            source, old, new, label, expected
        )

    # Adicionar campo de resposta numérica

    old_answers = '''        if (!reviewed) question.options.forEach((option, index) => {
            const button = document.createElement("button");
            button.type = "button";
            button.textContent = `${String.fromCharCode(65 + index)}) ${option}`;
            button.addEventListener("click", () => answerQuestion(question, index, button));
            answers.append(button);
        });'''

    new_answers = '''        if (!reviewed && question.type === "numeric") {
            const field = document.createElement("input");
            field.type = "text";
            field.inputMode = "decimal";
            field.className = "numeric-answer";

            field.setAttribute(
                "aria-label",
                `Resposta numérica em ${question.unit || "unidades"}`
            );

            field.placeholder =
                `Digite o valor (${question.unit || "número"})`;

            const send = document.createElement("button");
            send.type = "button";
            send.textContent = "Conferir cálculo";

            const submit = () => {
                const entered = field.value.trim().replace(",", ".");

                if (!entered || !Number.isFinite(Number(entered))) {
                    el("answerFeedback").textContent =
                        "Digite um número válido.";
                    return;
                }

                answerQuestion(question, Number(entered), send);

                if (!send.disabled) field.select();
            };

            send.addEventListener("click", submit);

            field.addEventListener("keydown", (event) => {
                if (event.key === "Enter") {
                    event.preventDefault();
                    submit();
                }
            });

            answers.append(field, send);

        } else if (!reviewed) question.options.forEach((option, index) => {
            const button = document.createElement("button");
            button.type = "button";

            button.textContent =
                `${String.fromCharCode(65 + index)}) ${option}`;

            button.addEventListener(
                "click",
                () => answerQuestion(question, index, button)
            );

            answers.append(button);
        });'''

    source = replace_exact(
        source, old_answers, new_answers, label
    )

    # Compatibilidade com usuários que já concluíram a fase 5

    source = replace_exact(
        source,
        '        return result;\n'
        '    }\n\n'
        '    let state = freshState();',

        '        if (result.stars["5"] > 0) '
        'result.unlocked = validPhases([...result.unlocked, 6]);\n'
        '        return result;\n'
        '    }\n\n'
        '    let state = freshState();',
        label
    )

    return source


# =========================================================
# 2. ATUALIZAR O BACKEND DJANGO
# =========================================================

def patch_views(source):
    label = "labcore_game/views.py"

    rules = [
        (
            'PHASES = ((1, "Equipamentos"), (2, "Química"), '
            '(3, "Física"), (4, "Biologia"), (5, "Desafio final"))',

            'PHASES = ((1, "Equipamentos"), (2, "Química"), '
            '(3, "Física"), (4, "Biologia"),\n'
            '          (5, "Revisão integrada"), '
            '(6, "Protocolos de laboratório"),\n'
            '          (7, "Análise de dados"), '
            '(8, "Missão cientista mestre"))',
            1
        ),
        (
            "phase = valid_int(item, 5)",
            "phase = valid_int(item, 8)",
            1
        ),
        (
            'current_phase = valid_int(data.get("current_phase", 1), 5)',
            'current_phase = valid_int(data.get("current_phase", 1), 8)',
            1
        ),
        (
            'key not in ("1", "2", "3", "4", "5")',
            'key not in tuple(str(i) for i in range(1, 9))',
            1
        ),
        (
            "for phase in range(1, 6)",
            "for phase in range(1, 9)",
            1
        ),
        (
            "Conclua as cinco fases antes de registrar no ranking",
            "Conclua as oito fases antes de registrar no ranking",
            1
        ),
        (
            '        if current_phase not in unlocked:\n'
            '            raise ValueError("A fase atual precisa estar desbloqueada")',

            '        if unlocked != list(range(1, max(unlocked) + 1)):\n'
            '            raise ValueError("Desbloqueio fora de sequência")\n'
            '        for phase in unlocked[1:]:\n'
            '            if stars.get(str(phase - 1), 0) < 1:\n'
            '                raise ValueError("Conclua a fase anterior")\n'
            '        if current_phase not in unlocked:\n'
            '            raise ValueError("A fase atual precisa estar desbloqueada")',
            1
        ),
        (
            'LeaderboardEntry.objects.select_related("user").order_by(',

            'LeaderboardEntry.objects.select_related('
            '"user", "user__game_progress").order_by(',
            1
        ),
        (
            '        if entry.user_id in seen:\n'
            '            continue\n'
            '        seen.add(entry.user_id)',

            '        if entry.user_id in seen:\n'
            '            continue\n'
            '        progress = getattr(entry.user, "game_progress", None)\n'
            '        if progress is None or any(\n'
            '            int(progress.phase_stars.get(str(p), 0)) < 1\n'
            '            for p in range(1, 9)\n'
            '        ):\n'
            '            continue\n'
            '        seen.add(entry.user_id)',
            1
        )
    ]

    for old, new, count in rules:
        source = replace_exact(
            source, old, new, label, count
        )

    return source


# =========================================================
# 3. CONECTAR OS ARQUIVOS NO HTML
# =========================================================

def patch_html(source):
    label = "templates/game.html"

    original = '''    <link rel="stylesheet" href="{% static 'labcore.css' %}">
    <script src="{% static 'labcore.js' %}" defer></script>'''

    updated = '''    <link rel="stylesheet" href="{% static 'labcore.css' %}">
    <link rel="stylesheet" href="{% static 'labcore-expansao.css' %}">
    <script src="{% static 'labcore-expansao.js' %}" defer></script>
    <script src="{% static 'labcore.js' %}" defer></script>'''

    source = replace_exact(
        source, original, updated, label
    )

    source = replace_exact(
        source,
        "<span>🧬 5 missões</span>",
        "<span>🧬 8 missões</span>",
        label
    )

    return source


# =========================================================
# 4. ATUALIZAR TESTES
# =========================================================

def patch_tests(source):
    label = "labcore_game/tests.py"

    rules = [
        (
            '"total_score": 650, "current_phase": 5,',
            '"total_score": 650, "current_phase": 8,'
        ),
        (
            '"unlocked_phases": [1, 2, 3, 4, 5],',
            '"unlocked_phases": list(range(1, 9)),'
        ),
        (
            "for i in range(1, 6)",
            "for i in range(1, 9)"
        ),
        (
            'json()["current_phase"], 5)',
            'json()["current_phase"], 8)'
        )
    ]

    for old, new in rules:
        source = replace_exact(
            source, old, new, label
        )

    return source


# =========================================================
# 5. CRIAR CENARIOS VETORIAIS DAS NOVAS FASES
# =========================================================

def make_svg(title):
    from xml.sax.saxutils import escape

    title = escape(title)

    return f'''<svg xmlns="http://www.w3.org/2000/svg"
        width="600" height="420" viewBox="0 0 600 420">
        <defs>
            <linearGradient id="g" x2="0" y2="1">
                <stop stop-color="#102942"/>
                <stop offset="1" stop-color="#041322"/>
            </linearGradient>
        </defs>

        <rect width="600" height="420"
            rx="28" fill="url(#g)"/>

        <rect x="45" y="80"
            width="510" height="280" rx="15"
            fill="#13334a" stroke="#4dcde9"
            stroke-width="5"/>

        <path d="M105 297 L495 297"
            stroke="#51e2ff" stroke-width="6"/>

        <path d="M165 270 L190 196 L217 270 Z"
            fill="#26b5db" stroke="white" stroke-width="4"/>

        <rect x="285" y="190" width="90" height="83"
            rx="8" fill="#246989"
            stroke="#70eeff" stroke-width="4"/>

        <circle cx="330" cy="230" r="20"
            fill="#82dfbe"/>

        <path d="M435 270 V200 l20 -35 20 35 v70 Z"
            fill="#4fc5e5" stroke="#fafafa"
            stroke-width="4"/>

        <text x="300" y="48" fill="#a2edff"
            font-size="27" font-family="Arial"
            font-weight="bold" text-anchor="middle">
            {title}
        </text>

        <text x="300" y="390" fill="#c8eaff"
            font-size="20" font-family="Arial"
            text-anchor="middle">
            LABCORE - INVESTIGACAO CIENTIFICA
        </text>
    </svg>'''


# =========================================================
# 6. INSTALACAO COM BACKUP
# =========================================================

def main():
    parser = argparse.ArgumentParser(
        description="Expansão LabCore para oito fases"
    )

    parser.add_argument(
        "repositorio",
        help="Caminho da pasta original do LabCore"
    )

    parser.add_argument(
        "--verificar",
        action="store_true",
        help="Verificar sem modificar o projeto"
    )

    args = parser.parse_args()

    target = Path(args.repositorio).expanduser().resolve()

    transforms = {
        "static/labcore.js": patch_javascript,
        "templates/game.html": patch_html,
        "labcore_game/views.py": patch_views,
        "labcore_game/tests.py": patch_tests,
        "templates/profile.html": lambda s: replace_exact(
            s, "/15", "/24", "templates/profile.html"
        )
    }

    outputs = {}

    # Confere todos os arquivos antes de alterar o projeto

    for path, transform in transforms.items():
        file = target / path

        if not file.is_file():
            raise SystemExit(
                f"Arquivo original não encontrado: {file}"
            )

        before = file.read_text(encoding="utf-8")
        outputs[path] = transform(before)

    # Os dois arquivos criados nas partes anteriores

    required = [
        ROOT / "labcore-expansao.js",
        ROOT / "labcore-expansao.css"
    ]

    for file in required:
        if not file.is_file():
            raise SystemExit(
                f"Arquivo ausente: {file.name}"
            )

    additions = {
        "static/labcore-expansao.js",
        "static/labcore-expansao.css",
        "static/assets/fase-protocolos.svg",
        "static/assets/fase-analise.svg",
        "static/assets/fase-mestre.svg"
    }

    if target == ROOT:
        raise SystemExit(
            "Selecione a pasta original do LabCore, "
            "não a pasta de atualização."
        )

    for path in additions:
        if (target / path).exists():
            raise SystemExit(
                f"O projeto já contém {path}. "
                "Instalação interrompida."
            )

    if args.verificar:
        print("Compatibilidade confirmada.")
        print("Arquivos originais verificados:", len(transforms))
        print("Novos arquivos:", len(additions))
        print("Nenhum arquivo foi alterado.")
        return

    # Criar backup antes das modificações

    stamp = datetime.datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup = (
        target.parent /
        f"{target.name}_backup_pre_8_fases_{stamp}"
    )

    backup.mkdir()

    for path in transforms:
        destination = backup / path

        destination.parent.mkdir(
            parents=True, exist_ok=True
        )

        shutil.copy2(
            target / path, destination
        )

    added = []

    try:
        # Atualiza arquivos originais

        for path, updated in outputs.items():
            (target / path).write_text(
                updated, encoding="utf-8"
            )

        # Copia arquivos novos e cria cenários

        for path in sorted(additions):
            destination = target / path

            destination.parent.mkdir(
                parents=True, exist_ok=True
            )

            if path.startswith("static/assets/"):
                title = {
                    "fase-protocolos.svg":
                        "PROTOCOLOS DE LABORATORIO",
                    "fase-analise.svg":
                        "ANALISE DE DADOS",
                    "fase-mestre.svg":
                        "CIENTISTA MESTRE"
                }[destination.name]

                destination.write_text(
                    make_svg(title),
                    encoding="utf-8"
                )

            else:
                shutil.copy2(
                    ROOT / Path(path).name,
                    destination
                )

            added.append(destination)

    except Exception:
        # Restaura arquivos originais em caso de erro

        for file in added:
            file.unlink(missing_ok=True)

        for path in transforms:
            shutil.copy2(
                backup / path,
                target / path
            )

        raise

    print()
    print("LABCORE ATUALIZADO PARA 8 FASES!")
    print("Backup criado em:", backup)
    print()
    print("Para testar:")
    print("py -3 manage.py test labcore_game")
    print()
    print("Para iniciar:")
    print("py -3 main.py")
    print()
    print("Acesse http://127.0.0.1:8000/")


if __name__ == "__main__":
    main()
