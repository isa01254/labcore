
/* LABCORE - EXPANSAO PARA 8 FASES
   Preserva as fases originais e acrescenta desafios.
*/
window.LabCoreExpansao = function expandirFases(phases) {
    "use strict";

    const extra = (id, name, x, y, q, options, correct, emoji = "🧪") => ({
        id, name, x, y, q, options, correct, emoji
    });

    const numerica = (
        id, name, x, y, q, answer, unit,
        emoji = "📊", tolerance = 0.01
    ) => ({
        id, name, x, y, q, type: "numeric",
        answer, unit, tolerance, emoji
    });

    // FASE 1 - EQUIPAMENTOS
    phases[1].difficulty = "Iniciante — identificação de equipamentos";
    phases[1].parSeconds = 240;

    // FASE 2 - QUIMICA
    phases[2].difficulty = "Básico — composição, pH e conservação da massa";
    phases[2].parSeconds = 210;

    phases[2].items.push(
        extra(
            "massa", "Conservação de massa", 150, 310,
            "Em um sistema fechado, 12 g de reagente A reagem com 8 g de B. Qual é a massa total dos produtos?",
            ["12 g", "16 g", "20 g", "24 g"],
            2, "⚗️"
        ),
        extra(
            "ph", "Escala de pH", 700, 310,
            "Uma solução com pH 3 tem quantas vezes mais íons H⁺ que outra de pH 5?",
            ["2 vezes", "10 vezes", "100 vezes", "1000 vezes"],
            2, "🧫"
        )
    );

    // FASE 3 - FISICA
    phases[3].difficulty = "Intermediário — circuitos e consumo de energia";
    phases[3].parSeconds = 200;

    phases[3].items.push(
        extra(
            "potencia", "Potência elétrica", 160, 310,
            "Um aparelho opera com tensão de 12 V e corrente de 2 A. Qual é sua potência?",
            ["6 W", "10 W", "14 W", "24 W"],
            3, "⚡"
        ),
        extra(
            "energia", "Consumo de energia", 720, 310,
            "Um equipamento de 200 W fica ligado por 3 h. Qual o consumo em kWh?",
            ["0,06 kWh", "0,6 kWh", "6 kWh", "60 kWh"],
            1, "🔋"
        )
    );

    // FASE 4 - BIOLOGIA
    phases[4].difficulty = "Intermediário avançado — processos celulares";
    phases[4].parSeconds = 195;

    phases[4].items.push(
        extra(
            "osmose", "Osmose", 160, 310,
            "Uma célula animal é colocada em solução hipertônica. O que tende a acontecer?",
            [
                "A célula ganha água",
                "A célula perde água",
                "O núcleo desaparece",
                "O DNA se duplica"
            ],
            1, "🧬"
        ),
        extra(
            "fotossintese", "Fotossíntese", 720, 310,
            "Qual combinação indica corretamente os reagentes consumidos na fotossíntese?",
            [
                "O₂ e glicose",
                "CO₂ e H₂O",
                "ATP e O₂",
                "Glicose e H₂O"
            ],
            1, "🌿"
        )
    );

    // FASE 5 - REVISAO INTEGRADA
    phases[5].name = "REVISÃO INTEGRADA";
    phases[5].difficulty = "Avançado — articulação de conceitos";
    phases[5].parSeconds = 205;

    phases[5].items.push(
        extra(
            "f5", "Método científico", 345, 310,
            "Um experimento compara plantas com e sem luz, mantendo água e solo iguais. Qual é a variável independente?",
            [
                "Crescimento",
                "Presença de luz",
                "Tipo de solo",
                "Quantidade de água"
            ],
            1, "🔍"
        ),
        extra(
            "f6", "Controle experimental", 565, 310,
            "Por que usar um grupo-controle em um experimento?",
            [
                "Garantir um resultado",
                "Evitar medições",
                "Criar referência para comparação",
                "Aumentar erros"
            ],
            2, "🧪"
        )
    );

    // FASE 6 - PROTOCOLOS DE LABORATORIO
    phases[6] = {
        name: "PROTOCOLOS DE LABORATÓRIO",
        difficulty: "Avançado — decisões e sequências experimentais",
        parSeconds: 250,
        art: "fase-protocolos.svg",
        items: [
            extra(
                "epi", "Segurança", 70, 120,
                "Antes de manipular solução irritante, qual conjunto de medidas é mais adequado?",
                [
                    "Avental e óculos, seguindo o protocolo",
                    "Luvas apenas",
                    "Trabalhar sem EPI",
                    "Cheirar a solução"
                ],
                0, "🥽"
            ),

            extra(
                "diluicao", "Diluição", 250, 120,
                "Para preparar uma solução 10 vezes mais diluída, qual procedimento é correto?",
                [
                    "Adicionar 10 vezes mais soluto",
                    "Misturar 1 parte de solução com 9 de diluente",
                    "Aquecer até ferver",
                    "Remover metade do solvente"
                ],
                1, "⚗️"
            ),

            extra(
                "contaminacao", "Contaminação", 430, 120,
                "Uma amostra biológica foi tocada com material não esterilizado. O que fazer?",
                [
                    "Ignorar o fato",
                    "Registrar e substituir a amostra conforme protocolo",
                    "Adicionar corante",
                    "Aquecer por 5 segundos"
                ],
                1, "🧫"
            ),

            extra(
                "variaveis", "Variáveis", 610, 120,
                "Ao testar o efeito da temperatura sobre uma reação, o que deve ser mantido constante?",
                [
                    "A temperatura",
                    "Todas as variáveis possíveis, exceto a temperatura",
                    "O resultado",
                    "O tempo de observação apenas"
                ],
                1, "📋"
            ),

            extra(
                "descarte", "Descarte", 790, 120,
                "Após uma prática com soluções químicas, qual é a conduta correta?",
                [
                    "Despejar tudo na pia",
                    "Misturar resíduos",
                    "Seguir a classificação e o procedimento de descarte",
                    "Guardar resíduos sem rótulo"
                ],
                2, "♻️"
            ),

            numerica(
                "volume", "Volume final", 430, 305,
                "Você mistura 15 mL de solução com 45 mL de água. Considerando volumes aditivos, qual é o volume final em mL? Digite apenas o número.",
                60, "mL", "🧪"
            )
        ]
    };

    // FASE 7 - ANALISE DE DADOS
    phases[7] = {
        name: "ANÁLISE DE DADOS",
        difficulty: "Especialista — cálculos, interpretação e evidências",
        parSeconds: 280,
        art: "fase-analise.svg",
        items: [
            numerica(
                "media", "Média de resultados", 70, 120,
                "Três medições deram 10, 14 e 18 unidades. Qual é a média aritmética? Digite apenas o número.",
                14, "unidades", "📊"
            ),

            numerica(
                "densidade", "Densidade", 250, 120,
                "Uma amostra tem massa de 84 g e volume de 28 mL. Qual é sua densidade em g/mL? Digite apenas o número.",
                3, "g/mL", "⚖️"
            ),

            extra(
                "hipotese", "Hipótese", 430, 120,
                "Em cinco testes, o grupo com luz cresceu mais. Qual conclusão é cientificamente adequada?",
                [
                    "Luz sempre causa crescimento em todas as plantas",
                    "Os dados sugerem associação neste experimento, sob as condições testadas",
                    "O teste comprovou qualquer situação",
                    "Não é necessário repetir"
                ],
                1, "🔎"
            ),

            numerica(
                "eficiencia", "Eficiência", 610, 120,
                "Em 40 tentativas, 30 produziram o resultado esperado. Qual foi o percentual de sucesso? Digite apenas o número.",
                75, "%", "📈"
            ),

            extra(
                "grafico", "Interpretação", 790, 120,
                "Uma curva cresce rapidamente e depois fica estável. O que o trecho horizontal indica?",
                [
                    "Aumento contínuo",
                    "Redução constante",
                    "Variação aproximadamente nula",
                    "Erro obrigatório no aparelho"
                ],
                2, "📉"
            ),

            extra(
                "replicacao", "Reprodutibilidade", 250, 305,
                "Qual ação fortalece a confiança em resultados experimentais?",
                [
                    "Repetir medições e documentar o método",
                    "Escolher apenas o melhor resultado",
                    "Omitir valores discrepantes sem análise",
                    "Trocar variáveis durante o teste"
                ],
                0, "📋"
            ),

            extra(
                "incerteza", "Incerteza", 610, 305,
                "Por que relatar a incerteza de uma medição?",
                [
                    "Porque torna a medida exata",
                    "Porque informa a precisão e as limitações do resultado",
                    "Porque dispensa unidades",
                    "Porque elimina erros sistemáticos"
                ],
                1, "📏"
            )
        ]
    };

    // FASE 8 - MISSAO FINAL
    phases[8] = {
        name: "MISSÃO CIENTISTA MESTRE",
        difficulty: "Mestre — resolução de problemas interdisciplinares",
        parSeconds: 330,
        art: "fase-mestre.svg",
        items: [
            numerica(
                "concentracao", "Concentração", 70, 120,
                "Uma solução contém 12 g de soluto em 300 mL de solução. Qual é a concentração em g/L? Digite apenas o número.",
                40, "g/L", "⚗️"
            ),

            numerica(
                "ohmfinal", "Circuito elétrico", 250, 120,
                "Dois resistores de 6 Ω e 3 Ω estão em paralelo. Qual é a resistência equivalente em Ω? Digite apenas o número.",
                2, "Ω", "⚡"
            ),

            extra(
                "amostra", "Amostragem", 430, 120,
                "Ao comparar duas culturas, por que usar o mesmo tempo de incubação?",
                [
                    "Para confundir variáveis",
                    "Para controlar um fator que poderia afetar o resultado",
                    "Para evitar registros",
                    "Para garantir crescimento idêntico"
                ],
                1, "🧫"
            ),

            numerica(
                "energiafinal", "Energia elétrica", 610, 120,
                "Uma lâmpada de 100 W fica acesa por 5 h. Qual é o consumo em kWh? Digite apenas o número.",
                0.5, "kWh", "🔋"
            ),

            extra(
                "biofinal", "Metabolismo celular", 790, 120,
                "Uma substância bloqueia a cadeia respiratória mitocondrial. Qual efeito direto é esperado?",
                [
                    "Aumento irrestrito de ATP",
                    "Redução da produção de ATP por fosforilação oxidativa",
                    "Produção de clorofila",
                    "Duplicação instantânea do DNA"
                ],
                1, "🧬"
            ),

            extra(
                "controlefinal", "Planejamento", 160, 305,
                "Para avaliar se um fertilizante melhora o crescimento, qual desenho experimental é mais adequado?",
                [
                    "Mudar água, luz e adubo juntos",
                    "Comparar grupos equivalentes com e sem adubo, mantendo os demais fatores",
                    "Avaliar apenas uma planta",
                    "Desconsiderar a duração"
                ],
                1, "🌱"
            ),

            numerica(
                "taxafinal", "Taxa experimental", 430, 305,
                "Uma população cresce de 80 para 100 em um período. Qual é o aumento percentual em relação ao valor inicial? Digite apenas o número.",
                25, "%", "📈"
            ),

            extra(
                "conclusao", "Relatório final", 700, 305,
                "Os resultados diferem da hipótese original. Qual é a atitude científica correta?",
                [
                    "Alterar os dados para concordar",
                    "Esconder os resultados",
                    "Relatar evidências, discutir limitações e revisar a hipótese",
                    "Descartar todos os registros"
                ],
                2, "🏆"
            )
        ]
    };
};
