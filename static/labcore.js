/* LabCore: jogo completo. As imagens originais ficam em static/assets/. */
(() => {
    "use strict";

    const app = document.getElementById("app");
    const assetRoot = app.dataset.assets;
    const loggedIn = app.dataset.auth === "1";
    const storageKey = `labcore_v3_${app.dataset.user}`;
    const csrf = document.querySelector('meta[name="csrf-token"]').content;
    const el = (id) => document.getElementById(id);
    const asset = (file) => assetRoot + encodeURIComponent(file);
    // SVG integrado para permitir jogar até sem internet/PNG, com aviso visível.
    function fallbackArt(label, symbol = "⚗") {
        const safe = String(label).replace(/[&<>"]/g, "");
        const svg = label === "Pesquisador"
            ? `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 112"><rect x="18" y="6" width="44" height="32" rx="8" fill="#5a3929" stroke="#22160f" stroke-width="3"/><rect x="17" y="27" width="46" height="27" rx="8" fill="#f1bb8d" stroke="#8d573c" stroke-width="2"/><rect x="27" y="37" width="4" height="4" fill="#182b3d"/><rect x="49" y="37" width="4" height="4" fill="#182b3d"/><rect x="20" y="54" width="40" height="37" rx="6" fill="#eafaff" stroke="#2c7293" stroke-width="3"/><rect x="3" y="56" width="16" height="36" rx="5" fill="#eafaff" stroke="#2c7293" stroke-width="3"/><rect x="61" y="56" width="16" height="36" rx="5" fill="#eafaff" stroke="#2c7293" stroke-width="3"/><rect x="25" y="90" width="13" height="18" fill="#315879"/><rect x="43" y="90" width="13" height="18" fill="#315879"/><rect x="20" y="105" width="21" height="5" fill="#081624"/><rect x="42" y="105" width="20" height="5" fill="#081624"/><rect x="38" y="57" width="4" height="25" fill="#2b8da8"/></svg>`
            : `<svg xmlns="http://www.w3.org/2000/svg" width="220" height="180" viewBox="0 0 220 180"><rect width="220" height="180" rx="16" fill="#092038"/><rect x="7" y="7" width="206" height="166" rx="12" fill="none" stroke="#38d9ff" stroke-width="2"/><text x="110" y="118" font-size="100" text-anchor="middle">${symbol}</text><text x="110" y="163" font-family="Arial" font-size="17" font-weight="bold" fill="#cff5ff" text-anchor="middle">${safe.slice(0, 24)}</text></svg>`;
        return "data:image/svg+xml;charset=utf-8," + encodeURIComponent(svg);
    }
    let warnedMissing = false;
    const failedImageUrls = new Set();
    function prepareImage(image, label, symbol = "⚗") {
        const replaceBrokenImage = () => {
            if (image.src.startsWith("data:")) return;
            failedImageUrls.add(image.getAttribute("src") || image.src);
            if (!warnedMissing) {
                warnedMissing = true;
                const warning = document.getElementById("assetWarning");
                if (warning) warning.hidden = false;
            }
            if (image.id === "background" || image.id === "sceneArt") {
                image.hidden = true;
                return;
            }
            image.src = fallbackArt(label, symbol);
        };
        image.addEventListener("error", replaceBrokenImage);
        // Imagens do HTML podem falhar antes de o script deferred executar.
        if (image.getAttribute("src") && image.complete && image.naturalWidth === 0) {
            replaceBrokenImage();
        }
        return image;
    }
    const aug = (time) => `Captura de tela 2026-08-31 ${time}.png`;
    const sep = (time) => `Captura de tela 2026-09-21 ${time}.png`;

    const sprites = {
        idle: aug("083221"), back: aug("083042"),
        walk1: aug("083055"), walk2: aug("083109"),
        run1: aug("083119"), run2: aug("083151"), run3: aug("083246"),
        alert: aug("083215"), point: aug("083255"), tablet: aug("083238"),
        victory: aug("083158")
    };
    Object.values(sprites).forEach((file) => {
        const preload = new Image();
        preload.src = asset(file);
    });

    const phases = {
        1: {
            name: "EQUIPAMENTOS", art: aug("083311"),
            items: [
                { id: "microscope", name: "Microscópio", x: 90, y: 120, img: sep("073857"),
                  q: "Qual equipamento permite observar estruturas muito pequenas, como células?",
                  options: ["Microscópio", "Termômetro", "Balança", "Béquer"], correct: 0 },
                { id: "computer", name: "Computador", x: 275, y: 120, img: aug("083306"),
                  q: "Qual equipamento é utilizado para processar e analisar dados?",
                  options: ["Microscópio", "Computador", "Centrífuga", "Pipeta"], correct: 1 },
                { id: "centrifuge", name: "Centrífuga", x: 460, y: 120, img: sep("073906"),
                  q: "Qual equipamento separa componentes de uma mistura usando rotação?",
                  options: ["Microscópio", "Termômetro", "Centrífuga", "Béquer"], correct: 2 },
                { id: "balance", name: "Balança", x: 650, y: 120, img: "balanca.svg",
                  q: "Qual equipamento é utilizado para medir a massa de uma amostra?",
                  options: ["Microscópio", "Termômetro", "Balança", "Béquer"], correct: 2 },
                { id: "pipette", name: "Micropipeta", x: 820, y: 120, img: sep("073950"),
                  q: "Qual instrumento permite transferir pequenos volumes de líquido com precisão?",
                  options: ["Balança", "Micropipeta", "Microscópio", "Placa de Petri"], correct: 1 },
                { id: "bunsen", name: "Bico de Bunsen", x: 125, y: 310, img: sep("073925"),
                  q: "Para qual atividade o bico de Bunsen pode ser utilizado sob supervisão?",
                  options: ["Aquecimento controlado", "Observação de células", "Medição de massa", "Centrifugação"], correct: 0 },
                { id: "petri", name: "Placa de Petri", x: 335, y: 310, img: sep("073938"),
                  q: "Qual material é frequentemente utilizado para cultivar microrganismos em laboratório?",
                  options: ["Termômetro", "Balança", "Placa de Petri", "Computador"], correct: 2 },
                { id: "flask", name: "Erlenmeyer", x: 545, y: 310, img: sep("073915"),
                  q: "Qual vidraria tem formato cônico e facilita a agitação de soluções?",
                  options: ["Pipeta", "Placa de Petri", "Lâmina", "Erlenmeyer"], correct: 3 },
                { id: "beaker", name: "Béquer", x: 755, y: 310, img: sep("073919"),
                  q: "Qual vidraria é comum para misturar líquidos e medir volumes aproximados?",
                  options: ["Béquer", "Microscópio", "Balança", "Computador"], correct: 0 }
            ]
        },
        2: {
            name: "QUÍMICA", art: aug("083324"),
            items: [
                { id: "h2o", name: "Água — H₂O", x: 150, y: 145, img: sep("073915"),
                  q: "Quais átomos formam uma molécula de água (H₂O)?",
                  options: ["2 de H e 1 de O", "1 de H e 2 de O", "1 de C e 2 de O", "1 de Na e 1 de Cl"], correct: 0 },
                { id: "nacl", name: "Sal — NaCl", x: 430, y: 310, img: sep("073911"),
                  q: "Quais elementos químicos formam o cloreto de sódio (NaCl)?",
                  options: ["Sódio e cloro", "Hidrogênio e cloro", "Sódio e oxigênio", "Carbono e cloro"], correct: 0 },
                { id: "co2", name: "CO₂", x: 725, y: 145, img: sep("074107"),
                  q: "Qual é a composição da molécula de dióxido de carbono (CO₂)?",
                  options: ["1 de C e 1 de O", "1 de C e 2 de O", "1 de C e 2 de H", "2 de C e 1 de O"], correct: 1 }
            ]
        },
        3: {
            name: "FÍSICA", art: aug("083340"),
            items: [
                { id: "ohm", name: "Lei de Ohm", x: 160, y: 145, img: sep("074127"),
                  q: "Se a tensão é 10 V e a corrente é 2 A, qual é a resistência?",
                  options: ["2 Ω", "5 Ω", "10 Ω", "20 Ω"], correct: 1 },
                { id: "serie", name: "Circuito em série", x: 425, y: 310, img: sep("074127"),
                  q: "Três resistores de 5 Ω em série têm qual resistência equivalente?",
                  options: ["5 Ω", "10 Ω", "15 Ω", "20 Ω"], correct: 2 },
                { id: "paralelo", name: "Circuito paralelo", x: 720, y: 145, img: sep("074127"),
                  q: "Dois resistores de 10 Ω em paralelo têm qual resistência equivalente?",
                  options: ["20 Ω", "10 Ω", "5 Ω", "2,5 Ω"], correct: 2 }
            ]
        },
        4: {
            name: "BIOLOGIA", art: aug("083318"),
            items: [
                { id: "nucleo", name: "Núcleo", x: 150, y: 145, img: sep("074100"),
                  q: "Qual estrutura celular contém o DNA e participa do controle das atividades celulares?",
                  options: ["Núcleo", "Mitocôndria", "Cloroplasto", "Membrana"], correct: 0 },
                { id: "mito", name: "Mitocôndria", x: 430, y: 310, img: sep("074100"),
                  q: "Qual organela está diretamente relacionada à produção de ATP na respiração celular?",
                  options: ["Núcleo", "Mitocôndria", "Cloroplasto", "Ribossomo"], correct: 1 },
                { id: "cloro", name: "Cloroplasto", x: 725, y: 145, img: sep("074113"),
                  q: "Nas células vegetais, qual organela realiza a fotossíntese?",
                  options: ["Núcleo", "Mitocôndria", "Cloroplasto", "Vacúolo"], correct: 2 }
            ]
        },
        5: {
            name: "DESAFIO FINAL", art: aug("083334"),
            items: [
                { id: "f1", name: "Equipamentos", x: 120, y: 130, img: sep("073857"),
                  q: "Desafio final: qual equipamento permite observar células?",
                  options: ["Microscópio", "Termômetro", "Balança", "Béquer"], correct: 0 },
                { id: "f2", name: "Química", x: 355, y: 130, img: sep("073919"),
                  q: "Desafio final: qual é a composição da água?",
                  options: ["2 de H e 1 de O", "1 de H e 2 de O", "1 de C e 2 de O", "Na e Cl"], correct: 0 },
                { id: "f3", name: "Física", x: 585, y: 130, img: sep("074127"),
                  q: "Desafio final: se V = 12 V e I = 3 A, qual é a resistência?",
                  options: ["3 Ω", "4 Ω", "6 Ω", "9 Ω"], correct: 1 },
                { id: "f4", name: "Biologia", x: 760, y: 310, img: sep("074113"),
                  q: "Desafio final: qual organela das células vegetais realiza a fotossíntese?",
                  options: ["Núcleo", "Mitocôndria", "Cloroplasto", "Ribossomo"], correct: 2 }
            ]
        }
    };

    // Arte adicional do mapa, reaproveitando a captura do pesquisador com tablet.
    const mapArt = prepareImage(new Image(), "Mapa de missões", "🗺");
    mapArt.src = asset(sprites.tablet);
    mapArt.alt = "Pesquisador consultando o mapa de missões";
    mapArt.className = "hero small";
    mapArt.style.height = "82px";
    el("mapScreen").insertBefore(mapArt, el("mapScreen").firstChild);

    const freshState = () => ({
        phase: 1, score: 0, unlocked: [1], stars: {},
        phaseScores: {}, times: {}, done: {}, claimed: {}, bonus: {}, correct: 0, mistakes: 0
    });
    const objectLike = (value) => value && typeof value === "object" && !Array.isArray(value);
    const integer = (value, fallback = 0, max = 10000000) =>
        Number.isSafeInteger(Number(value)) && Number(value) >= 0
            ? Math.min(Number(value), max) : fallback;
    const validPhases = (values) => [1, ...(
        Array.isArray(values) ? values.filter((n) => Number.isInteger(n) && n >= 1 && n <= 5) : []
    )].filter((number, index, array) => array.indexOf(number) === index).sort((a, b) => a - b);

    function normalized(raw) {
        const result = freshState();
        if (!objectLike(raw)) return result;
        result.phase = integer(raw.phase, 1, 5) || 1;
        result.score = integer(raw.score);
        result.unlocked = validPhases(raw.unlocked);
        result.correct = integer(raw.correct);
        result.mistakes = integer(raw.mistakes);
        const stars = objectLike(raw.stars) ? raw.stars : {};
        const scores = objectLike(raw.phaseScores) ? raw.phaseScores : {};
        const done = objectLike(raw.done) ? raw.done : {};
        const claimed = objectLike(raw.claimed) ? raw.claimed : {};
        const bonuses = objectLike(raw.bonus) ? raw.bonus : {};
        const times = objectLike(raw.times) ? raw.times : {};
        for (let phase = 1; phase <= 5; phase++) {
            const key = String(phase);
            result.stars[key] = integer(stars[key], 0, 3);
            result.times[key] = integer(times[key]);
            const value = scores[key];
            const fromScore = objectLike(value) && Array.isArray(value.done) ? value.done : [];
            const allowed = phases[phase].items.map((item) => item.id);
            result.done[key] = [...new Set([...(Array.isArray(done[key]) ? done[key] : []), ...fromScore])]
                .filter((id) => allowed.includes(id));
            const earned = objectLike(value) && Array.isArray(value.claimed) ? value.claimed : [];
            result.claimed[key] = [...new Set([
                ...(Array.isArray(claimed[key]) ? claimed[key] : []), ...earned, ...result.done[key]
            ])].filter((id) => allowed.includes(id));
            result.bonus[key] = integer(objectLike(value) ? value.bonus : bonuses[key], 0, 50);
            result.phaseScores[key] = {
                score: integer(objectLike(value) ? value.score : value),
                done: result.done[key], claimed: result.claimed[key], bonus: result.bonus[key]
            };
        }
        return result;
    }

    let state = freshState();
    let mode = "menu";
    let modalOpen = false;
    let currentQuestion = null;
    let near = null;
    let player = { x: 70, y: 350, width: 58, height: 82 };
    let keys = new Set();
    let phaseStart = 0;
    let phaseMistakesStart = 0;
    let timer = null;
    let lastFrame = 0;
    let currentSprite = "";
    let serverQueue = Promise.resolve();
    let phaseStarted = false;

    function doneList(phase = state.phase) {
        return state.done[String(phase)] || [];
    }
    function saveLocal() {
        try { localStorage.setItem(storageKey, JSON.stringify(state)); }
        catch (error) { console.warn("Progresso local indisponível:", error); }
    }
    function loadLocal() {
        try {
            // Importa o salvamento da versão antiga somente na primeira abertura.
            const saved = localStorage.getItem(storageKey) || (loggedIn ? null : localStorage.getItem("labcore"));
            if (saved) state = normalized(JSON.parse(saved));
        } catch (error) { console.warn("Progresso anterior inválido:", error); }
    }
    function saveRemote(completed = false) {
        if (!loggedIn) return Promise.resolve();
        const payload = {
            total_score: state.score, current_phase: state.phase,
            unlocked_phases: state.unlocked, phase_scores: state.phaseScores,
            phase_stars: state.stars, phase_times: state.times,
            correct_answers: state.correct, mistakes: state.mistakes,
            game_completed: completed
        };
        serverQueue = serverQueue.catch(() => {}).then(async () => {
            const response = await fetch("/api/save/", {
                method: "POST", credentials: "same-origin",
                headers: { "Content-Type": "application/json", "X-CSRFToken": csrf },
                body: JSON.stringify(payload)
            });
            if (!response.ok) throw Error(`Falha ao salvar: HTTP ${response.status}`);
        });
        serverQueue.catch((error) => console.warn(error));
        return serverQueue;
    }
    async function loadRemote() {
        if (!loggedIn) return;
        try {
            const response = await fetch("/api/load/", { credentials: "same-origin" });
            if (!response.ok) throw Error(`HTTP ${response.status}`);
            const data = await response.json();
            if (!data.ok || phaseStarted) return;
            const remote = normalized({
                phase: data.current_phase, score: data.total_score,
                unlocked: data.unlocked_phases, stars: data.phase_stars,
                phaseScores: data.phase_scores, times: data.phase_times,
                correct: data.correct_answers, mistakes: data.mistakes
            });
            state.score = Math.max(state.score, remote.score);
            state.correct = Math.max(state.correct, remote.correct);
            state.mistakes = Math.max(state.mistakes, remote.mistakes);
            state.unlocked = validPhases([...state.unlocked, ...remote.unlocked]);
            if (remote.phase > state.phase) state.phase = remote.phase;
            for (let phase = 1; phase <= 5; phase++) {
                const key = String(phase);
                state.stars[key] = Math.max(integer(state.stars[key], 0, 3), remote.stars[key]);
                const localTime = integer(state.times[key]);
                const remoteTime = integer(remote.times[key]);
                if (remoteTime) state.times[key] = localTime ? Math.min(localTime, remoteTime) : remoteTime;
                state.done[key] = [...new Set([...doneList(phase), ...remote.done[key]])];
                state.claimed[key] = [...new Set([
                    ...(state.claimed[key] || []), ...(remote.claimed[key] || []), ...state.done[key]
                ])];
                state.bonus[key] = Math.max(integer(state.bonus[key], 0, 50), integer(remote.bonus[key], 0, 50));
                state.phaseScores[key] = {
                    score: Math.max(integer(state.phaseScores[key]?.score), remote.phaseScores[key].score),
                    done: state.done[key], claimed: state.claimed[key], bonus: state.bonus[key]
                };
            }
            saveLocal(); updateHUD();
            if (mode === "map") renderMap();
        } catch (error) { console.warn("Progresso remoto indisponível:", error); }
    }

    const screensForMobile = ["menuScreen", "mapScreen", "rankingScreen", "resultScreen"];
    function fitStage() {
        const viewportWidth = Math.min(window.innerWidth, window.screen?.width || window.innerWidth);
        const mobile = viewportWidth <= 700;
        for (const id of screensForMobile) {
            const screen = el(id);
            const target = mobile ? document.body : el("world");
            if (screen.parentElement !== target) target.append(screen);
            screen.classList.toggle("mobile-screen", mobile);
        }
        const scale = Math.min(1, Math.max(0.28, (viewportWidth - 20) / 960));
        el("stage").style.width = `${960 * scale}px`;
        el("stage").style.height = `${540 * scale}px`;
        el("world").style.transform = `scale(${scale})`;
    }
    function setSprite(name, flip = false) {
        const signature = `${name}/${flip}`;
        if (signature === currentSprite) return;
        currentSprite = signature;
        const requested = asset(sprites[name]);
        el("player").src = failedImageUrls.has(requested)
            ? fallbackArt("Pesquisador", "👩‍🔬") : requested;
        el("player").style.transform = flip ? "scaleX(-1)" : "none";
    }
    function placePlayer() {
        el("player").style.left = `${player.x}px`;
        el("player").style.top = `${player.y}px`;
    }
    function updateHUD() {
        el("topScore").textContent = state.score;
        el("hudScore").textContent = state.score;
        el("hudPhase").textContent = `FASE ${state.phase} — ${phases[state.phase].name}`;
        el("hudProgress").textContent = `${doneList().length}/${phases[state.phase].items.length}`;
    }
    function showScreen(next) {
        mode = next;
        const screens = { menu: "menuScreen", map: "mapScreen", ranking: "rankingScreen", result: "resultScreen" };
        Object.entries(screens).forEach(([name, id]) => { el(id).hidden = name !== next; });
        el("hud").hidden = next !== "play";
        el("player").hidden = next !== "play";
        el("objects").hidden = next !== "play";
        el("sceneArt").hidden = next !== "play";
        el("touchControls").hidden = next !== "play";
        el("nearPrompt").hidden = true;
        el("questionOverlay").hidden = true;
        modalOpen = false;
        currentQuestion = null;
        near = null;
        keys.clear();
        if (next !== "play") { clearInterval(timer); timer = null; }
        if (next === "map") renderMap();
        updateHUD();
    }
    function renderMap() {
        const cards = el("phaseCards");
        cards.replaceChildren();
        Object.entries(phases).forEach(([key, phase]) => {
            const id = Number(key);
            const unlocked = state.unlocked.includes(id);
            const stars = integer(state.stars[key], 0, 3);
            const button = document.createElement("button");
            button.type = "button";
            button.className = "phase-card";
            button.disabled = !unlocked;
            const image = prepareImage(document.createElement("img"), phase.name, "🧪");
            image.src = asset(phase.art);
            image.alt = "";
            const name = document.createElement("strong");
            name.textContent = `${id}. ${phase.name}`;
            const starline = document.createElement("span");
            starline.className = "starline";
            starline.textContent = "★".repeat(stars) + "☆".repeat(3 - stars);
            const note = document.createElement("small");
            note.textContent = !unlocked ? "BLOQUEADA" : stars ? "CONCLUÍDA · REJOGAR" : "DISPONÍVEL";
            button.append(image, name, starline, note);
            button.addEventListener("click", () => startPhase(id));
            cards.append(button);
        });
    }
    function buildLaboratory() {
        const objects = el("objects");
        objects.replaceChildren();
        for (const question of phases[state.phase].items) {
            const button = document.createElement("button");
            button.type = "button";
            button.className = "object";
            button.style.left = `${question.x}px`;
            button.style.top = `${question.y}px`;
            button.dataset.id = question.id;
            button.setAttribute("aria-label", `Abrir desafio: ${question.name}`);
            if (doneList().includes(question.id)) button.classList.add("done");
            if (question.img) {
                const image = prepareImage(document.createElement("img"), question.name, "🔬");
                image.src = asset(question.img);
                image.alt = "";
                button.append(image);
            } else {
                const emoji = document.createElement("span");
                emoji.className = "emoji";
                emoji.textContent = question.emoji || "🧪";
                button.append(emoji);
            }
            const title = document.createElement("span");
            title.className = "object-name";
            title.textContent = question.name;
            button.append(title);
            button.addEventListener("click", () => openQuestion(question.id));
            objects.append(button);
        }
        el("sceneArt").hidden = false;
        el("sceneArt").src = asset(phases[state.phase].art);
        // A pipeta e o bico de Bunsen também usam as capturas originais.
        el("world").querySelector(".ambient-lab")?.remove();
        const extra = state.phase === 1 ? sep("073950") :
                      state.phase === 2 ? sep("073925") : null;
        if (extra) {
            const decoration = document.createElement("img");
            decoration.className = "ambient-lab";
            prepareImage(decoration, "Equipamento", "🧪");
            decoration.src = asset(extra);
            decoration.alt = "";
            Object.assign(decoration.style, {
                position: "absolute", zIndex: "2", left: "810px", top: "175px",
                width: "88px", height: "100px", objectFit: "contain",
                imageRendering: "pixelated", opacity: ".68", pointerEvents: "none"
            });
            el("world").append(decoration);
        }
    }
    function startPhase(id) {
        if (!phases[id] || !state.unlocked.includes(id)) return;
        const previousDone = state.done[String(id)] || [];
        if (previousDone.length === phases[id].items.length && integer(state.stars[String(id)]) > 0) {
            if (!window.confirm("Esta fase já foi concluída. Deseja jogá-la novamente?")) return;
            state.done[String(id)] = [];
            const previous = state.phaseScores[String(id)] || {};
            state.phaseScores[String(id)] = {
                score: integer(previous.score), done: [],
                claimed: state.claimed[String(id)] || [], bonus: integer(state.bonus[String(id)], 0, 50)
            };
        }
        phaseStarted = true;
        state.phase = id;
        phaseMistakesStart = state.mistakes;
        player = { x: 70, y: 350, width: 58, height: 82 };
        near = null;
        phaseStart = Date.now();
        setSprite("idle");
        placePlayer();
        buildLaboratory();
        showScreen("play");
        timer = setInterval(updateTime, 250);
        updateTime();
        saveLocal();
    }
    function updateTime() {
        const seconds = Math.floor((Date.now() - phaseStart) / 1000);
        el("hudTime").textContent = `${String(Math.floor(seconds / 60)).padStart(2, "0")}:${String(seconds % 60).padStart(2, "0")}`;
    }
    function openQuestion(id) {
        if (mode !== "play" || modalOpen) return;
        const question = phases[state.phase].items.find((item) => item.id === id);
        if (!question) return;
        const reviewed = doneList().includes(id);
        currentQuestion = reviewed ? null : question;
        modalOpen = true;
        keys.clear();
        el("questionTitle").textContent = `${phases[state.phase].name} — ${question.name}`;
        el("questionText").textContent = reviewed
            ? `${question.q} Resposta: ${question.options[question.correct]}.`
            : question.q;
        el("answerFeedback").textContent = "";
        el("answerFeedback").className = "answer-feedback";
        el("questionImage").hidden = !question.img;
        el("questionImage").classList.remove("enlarged");
        if (question.img) {
            el("questionImage").src = asset(question.img);
            el("questionImage").alt = question.name;
        }
        const answers = el("answerButtons");
        answers.replaceChildren();
        if (reviewed) {
            const back = document.createElement("button");
            back.type = "button";
            back.textContent = "✓ Entendi — voltar ao laboratório";
            back.addEventListener("click", closeQuestion);
            answers.append(back);
        }
        if (!reviewed) question.options.forEach((option, index) => {
            const button = document.createElement("button");
            button.type = "button";
            button.textContent = `${String.fromCharCode(65 + index)}) ${option}`;
            button.addEventListener("click", () => answerQuestion(question, index, button));
            answers.append(button);
        });
        setSprite("point");
        el("questionOverlay").hidden = false;
        answers.querySelector("button")?.focus();
    }
    function closeQuestion() {
        modalOpen = false;
        currentQuestion = null;
        el("questionOverlay").hidden = true;
        keys.clear();
    }
    function answerQuestion(question, index, button) {
        if (mode !== "play" || !modalOpen || currentQuestion?.id !== question.id || doneList().includes(question.id)) return;
        const feedback = el("answerFeedback");
        if (index !== question.correct) {
            if (button.disabled) return;
            button.disabled = true;
            state.mistakes++;
            feedback.className = "answer-feedback wrong";
            feedback.textContent = "Resposta incorreta. Tente outra alternativa.";
            saveLocal(); void saveRemote();
            return;
        }
        el("answerButtons").querySelectorAll("button").forEach((option) => { option.disabled = true; });
        state.correct++;
        const key = String(state.phase);
        const claimed = state.claimed[key] || [];
        const newlyEarned = !claimed.includes(question.id);
        if (newlyEarned) {
            state.score += 100;
            state.claimed[key] = [...claimed, question.id];
        }
        state.done[key] = [...doneList(), question.id];
        state.phaseScores[key] = {
            score: integer(state.phaseScores[key]?.score) + (newlyEarned ? 100 : 0),
            done: state.done[key], claimed: state.claimed[key] || [], bonus: integer(state.bonus[key], 0, 50)
        };
        el("objects").querySelectorAll(".object").forEach((object) => {
            if (object.dataset.id === question.id) object.classList.add("done");
        });
        feedback.className = "answer-feedback correct";
        feedback.textContent = newlyEarned ? "Resposta correta! +100 XP" : "Resposta correta! Questão já pontuada anteriormente.";
        updateHUD(); saveLocal(); void saveRemote();
        const phaseAnswered = state.phase;
        setTimeout(() => {
            if (mode !== "play" || state.phase !== phaseAnswered) return;
            if (currentQuestion && currentQuestion.id !== question.id) return;
            closeQuestion();
            if (doneList().length === phases[phaseAnswered].items.length) finishPhase();
        }, 650);
    }
    function finishPhase() {
        clearInterval(timer); timer = null;
        const seconds = Math.max(1, Math.floor((Date.now() - phaseStart) / 1000));
        const errors = state.mistakes - phaseMistakesStart;
        const bonus = seconds <= 60 ? 50 : seconds <= 120 ? 25 : 0;
        const stars = errors >= 3 ? 1 : seconds <= 90 && errors === 0 ? 3 : 2;
        const key = String(state.phase);
        const previousBonus = integer(state.bonus[key], 0, 50);
        const newBonus = Math.max(previousBonus, bonus);
        const bonusEarned = newBonus - previousBonus;
        state.bonus[key] = newBonus;
        state.score += bonusEarned;
        state.phaseScores[key] = {
            score: integer(state.phaseScores[key]?.score) + bonusEarned,
            done: doneList(), claimed: state.claimed[key] || [], bonus: newBonus
        };
        state.stars[key] = Math.max(integer(state.stars[key], 0, 3), stars);
        const oldTime = integer(state.times[key]);
        state.times[key] = oldTime ? Math.min(oldTime, seconds) : seconds;
        if (state.phase < 5) state.unlocked = validPhases([...state.unlocked, state.phase + 1]);
        const completed = state.phase === 5 && [1, 2, 3, 4, 5].every((phase) => integer(state.stars[String(phase)]) > 0);
        el("resultTitle").textContent = completed ? "LABORATÓRIO CONCLUÍDO!" : "FASE CONCLUÍDA!";
        el("resultStars").textContent = "★".repeat(stars) + "☆".repeat(3 - stars);
        el("resultText").textContent = `Pontuação total: ${state.score} XP · Bônus desta rodada: +${bonusEarned} XP · Tempo: ${seconds}s`;
        el("resultNext").textContent = state.phase === 5 ? "Voltar ao mapa" : "Próxima fase";
        setSprite("victory");
        showScreen("result");
        saveLocal(); void saveRemote(completed);
    }
    async function showRanking() {
        showScreen("ranking");
        const rows = el("rankingRows");
        rows.textContent = "Carregando ranking...";
        try {
            const response = await fetch("/api/leaderboard/");
            if (!response.ok) throw Error(`HTTP ${response.status}`);
            const data = await response.json();
            if (mode !== "ranking") return;
            rows.replaceChildren();
            if (!Array.isArray(data.leaderboard) || !data.leaderboard.length) {
                rows.textContent = "Ainda não há jogadores no ranking. Cadastre-se e conclua as cinco fases!";
                return;
            }
            data.leaderboard.forEach((entry, index) => {
                const row = document.createElement("div");
                row.className = "rank-row";
                const name = document.createElement("span");
                name.textContent = `#${index + 1} ${entry.username}`;
                const score = document.createElement("span");
                score.textContent = `${integer(entry.score)} XP`;
                row.append(name, score);
                rows.append(row);
            });
        } catch (error) {
            if (mode === "ranking") rows.textContent = "Não foi possível carregar o ranking.";
            console.warn(error);
        }
    }
    function interact() { if (near && mode === "play" && !modalOpen) openQuestion(near.id); }
    function moveFrame(now) {
        const seconds = lastFrame ? Math.min(0.05, (now - lastFrame) / 1000) : 0;
        lastFrame = now;
        if (mode === "play" && !modalOpen) {
            const dx = Number(keys.has("d") || keys.has("arrowright")) - Number(keys.has("a") || keys.has("arrowleft"));
            const dy = Number(keys.has("s") || keys.has("arrowdown")) - Number(keys.has("w") || keys.has("arrowup"));
            const moving = dx !== 0 || dy !== 0;
            if (moving) {
                const speed = 215 * seconds / Math.hypot(dx, dy);
                player.x = Math.max(16, Math.min(960 - player.width - 16, player.x + dx * speed));
                player.y = Math.max(65, Math.min(540 - player.height - 16, player.y + dy * speed));
                placePlayer();
            }
            const nearest = phases[state.phase].items
                .filter((q) => !doneList().includes(q.id))
                .map((q) => ({ ...q, distance: Math.hypot(player.x + 29 - q.x - 48, player.y + 41 - q.y - 50) }))
                .sort((a, b) => a.distance - b.distance)[0];
            near = nearest && nearest.distance < 110 ? nearest : null;
            el("nearPrompt").hidden = !near;
            if (near) el("nearPrompt").textContent = `Pressione E para interagir: ${near.name}`;
            el("objects").querySelectorAll(".object").forEach((object) => {
                object.classList.toggle("near", Boolean(near && object.dataset.id === near.id));
            });
            let sprite = "idle";
            if (moving) {
                if (dy < 0 && dx === 0) sprite = "back";
                else sprite = ["walk1", "walk2", "run1", "run2", "run3"][Math.floor(now / 140) % 5];
            } else if (near) sprite = "alert";
            setSprite(sprite, dx < 0);
        }
        requestAnimationFrame(moveFrame);
    }

    // Botões do menu e do mapa.
    el("playButton").addEventListener("click", () => showScreen("map"));
    el("mapButton").addEventListener("click", () => showScreen("map"));
    el("rankingButton").addEventListener("click", showRanking);
    el("mapBack").addEventListener("click", () => showScreen("menu"));
    el("rankingBack").addEventListener("click", () => showScreen("menu"));
    el("resultMap").addEventListener("click", () => showScreen("map"));
    el("resultNext").addEventListener("click", () => {
        if (state.phase === 5) showScreen("map");
        else startPhase(state.phase + 1);
    });
    el("closeQuestion").addEventListener("click", closeQuestion);
    el("questionImage").setAttribute("role", "button");
    el("questionImage").setAttribute("tabindex", "0");
    el("questionImage").setAttribute("aria-label", "Ampliar ou reduzir imagem");
    function zoomQuestionImage() {
        el("questionImage").classList.toggle("enlarged");
    }
    el("questionImage").addEventListener("click", zoomQuestionImage);
    el("questionImage").addEventListener("keydown", (event) => {
        if (event.key === "Enter" || event.key === " ") {
            event.preventDefault(); zoomQuestionImage();
        }
    });

    // Teclado: W/A/S/D, setas, E e Escape.
    const movementKeys = new Set(["w", "a", "s", "d", "arrowup", "arrowdown", "arrowleft", "arrowright"]);
    document.addEventListener("keydown", (event) => {
        const key = event.key.toLowerCase();
        if (event.repeat && (key === "e" || key === "escape")) return;
        if (key === "escape") {
            if (modalOpen) closeQuestion();
            else if (mode === "play" || mode === "result") showScreen("map");
            else if (mode === "map" || mode === "ranking") showScreen("menu");
            return;
        }
        if (mode !== "play" || modalOpen) return;
        if (movementKeys.has(key)) { event.preventDefault(); keys.add(key); }
        if (key === "e") { event.preventDefault(); interact(); }
    });
    document.addEventListener("keyup", (event) => keys.delete(event.key.toLowerCase()));
    window.addEventListener("blur", () => keys.clear());

    // Controles de toque (celular/tablet).
    el("touchControls").querySelectorAll("[data-key]").forEach((button) => {
        const key = button.dataset.key;
        button.addEventListener("pointerdown", (event) => {
            event.preventDefault();
            button.setPointerCapture(event.pointerId);
            keys.add(key);
        });
        ["pointerup", "pointercancel", "lostpointercapture"].forEach((name) =>
            button.addEventListener(name, () => keys.delete(key)));
    });
    el("touchInteract").addEventListener("click", interact);
    el("touchMap").addEventListener("click", () => showScreen("map"));
    window.addEventListener("resize", fitStage);
    window.addEventListener("pagehide", saveLocal);

    // Capturas do HTML também usam o mesmo fallback quando faltarem assets.
    prepareImage(el("background"), "Laboratório", "⚗");
    prepareImage(el("player"), "Pesquisador", "👩‍🔬");
    prepareImage(el("sceneArt"), "Cena do laboratório", "🧪");
    prepareImage(el("questionImage"), "Equipamento", "🔬");
    document.querySelectorAll(".hero").forEach((image) => prepareImage(image, "Pesquisador", "👩‍🔬"));
    loadLocal();
    fitStage();
    showScreen("menu");
    void loadRemote();
    requestAnimationFrame(moveFrame);
})();
