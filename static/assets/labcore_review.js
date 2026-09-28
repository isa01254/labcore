(function () {
    "use strict";

    const spriteName = {
        idle: "Captura de tela 2026-08-31 083221.png",
        back: "Captura de tela 2026-08-31 083042.png",
        walk1: "Captura de tela 2026-08-31 083055.png",
        walk2: "Captura de tela 2026-08-31 083109.png",
        run1: "Captura de tela 2026-08-31 083119.png",
        run2: "Captura de tela 2026-08-31 083151.png",
        alert: "Captura de tela 2026-08-31 083215.png",
        point: "Captura de tela 2026-08-31 083255.png",
        tablet: "Captura de tela 2026-08-31 083238.png",
        victory: "Captura de tela 2026-08-31 083158.png"
    };

    const phasePicture = {
        1: "Captura de tela 2026-08-31 083311.png",
        2: "Captura de tela 2026-08-31 083324.png",
        3: "Captura de tela 2026-08-31 083340.png",
        4: "Captura de tela 2026-08-31 083318.png",
        5: "Captura de tela 2026-08-31 083334.png"
    };

    const objectPicture = {
        microscope: "Captura de tela 2026-09-21 073857.png",
        computer: "Captura de tela 2026-08-31 083306.png",
        centrifuge: "Captura de tela 2026-09-21 073906.png",
        balance: "Captura de tela 2026-09-21 073911.png",
        h2o: "Captura de tela 2026-09-21 073915.png",
        nacl: "Captura de tela 2026-09-21 073911.png",
        co2: "Captura de tela 2026-09-21 073919.png",
        ohm: "Captura de tela 2026-09-21 074127.png",
        serie: "Captura de tela 2026-09-21 074127.png",
        paralelo: "Captura de tela 2026-09-21 074127.png",
        nucleo: "Captura de tela 2026-09-21 074100.png",
        mito: "Captura de tela 2026-09-21 074100.png",
        cloro: "Captura de tela 2026-09-21 074113.png",
        f1: "Captura de tela 2026-09-21 073857.png",
        f2: "Captura de tela 2026-09-21 073915.png",
        f3: "Captura de tela 2026-09-21 074127.png",
        f4: "Captura de tela 2026-09-21 074113.png"
    };

    const picture = (filename) =>
        window.LABCORE_ASSET_BASE + encodeURIComponent(filename);

    function makeImage(filename, cssClass, alt) {
        const img = document.createElement("img");
        img.src = picture(filename);
        img.className = cssClass;
        img.alt = alt || "";
        img.decoding = "async";
        img.addEventListener("error", () => {
            img.hidden = true;
        }, { once: true });
        return img;
    }

    const background = document.getElementById("laboratoryBackground");
    if (background) {
        background.src = picture("Laboratório Sci-Fi Neon em Pixel Art.png");
    }

    player.width = 46;
    player.height = 60;

    function setPlayerSprite(name, flip = false) {
        if (!playerElement) return;
        playerElement.style.setProperty(
            "background-image",
            `url("${picture(spriteName[name])}")`,
            "important"
        );
        playerElement.style.transform = flip ? "scaleX(-1)" : "none";
    }

    setPlayerSprite("idle");

    const menuArt = makeImage(
        spriteName.alert,
        "labcore-menu-image",
        "Pesquisador LabCore"
    );

    const mapArt = makeImage(
        spriteName.tablet,
        "labcore-map-image",
        "Mapa de missões"
    );

    const mainSubtitle = mainMenu.querySelector(".screen-subtitle");
    if (mainSubtitle) {
        mainSubtitle.insertAdjacentElement("afterend", menuArt);
    }

    const mapSubtitle = mapScreen.querySelector(".screen-subtitle");
    if (mapSubtitle) {
        mapSubtitle.insertAdjacentElement("afterend", mapArt);
    }

    const scene = makeImage(
        phasePicture[1],
        "",
        "Cena do laboratório"
    );
    scene.id = "labcoreScene";
    scene.style.display = "none";
    wrap.appendChild(scene);

    const originalRenderMap = renderMap;
    renderMap = function () {
        originalRenderMap();

        document.querySelectorAll("#mapBtns .phase-button").forEach((button, index) => {
            const phase = index + 1;
            if (button.querySelector(".labcore-phase-image")) return;

            const img = makeImage(
                phasePicture[phase],
                "labcore-phase-image",
                `Fase ${phase}`
            );

            const phaseName = button.querySelector(".phase-name");
            if (phaseName) {
                button.insertBefore(img, phaseName);
            }
        });
    };

    const originalBuildLaboratory = buildLaboratory;
    buildLaboratory = function (phase) {
        originalBuildLaboratory(phase);

        document.querySelectorAll("#gameWrap .obj").forEach((obj) => {
            const challenge = CHALLENGES[phase].find(item => item.id === obj.dataset.id);
            if (!challenge) return;

            const filename = objectPicture[challenge.id];
            if (filename && !obj.querySelector(".labcore-object-image")) {
                const oldIcon = obj.querySelector("span:not(.obj-label)");
                const img = makeImage(filename, "labcore-object-image", challenge.label);

                if (oldIcon) {
                    oldIcon.replaceWith(img);
                } else {
                    obj.insertBefore(img, obj.firstChild);
                }
            }

            obj.style.cursor = "pointer";
            obj.onclick = () => openChallenge(challenge.id);
        });

        scene.src = picture(phasePicture[phase]);
        scene.style.display = "block";
    };

    const originalOpenChallenge = openChallenge;
    openChallenge = function (id) {
        const challenge = CHALLENGES[state.phase].find(item => item.id === id);
        if (!challenge || phaseDone.includes(id)) return;

        originalOpenChallenge(id);
        setPlayerSprite("point");

        const old = document.getElementById("labcoreChallengePicture");
        if (old) old.remove();

        const filename = objectPicture[id];
        if (filename) {
            const img = makeImage(filename, "labcore-challenge-image", challenge.label);
            img.id = "labcoreChallengePicture";
            document.getElementById("qText").insertAdjacentElement("beforebegin", img);
        }
    };

    const originalStartPhase = startPhase;
    startPhase = function (phase) {
        originalStartPhase(phase);
        player.x = 66;
        player.y = 280;
        playerElement.style.left = player.x + "px";
        playerElement.style.top = player.y + "px";
        setPlayerSprite("idle");
    };

    const originalFinishPhase = finishPhase;
    finishPhase = function () {
        originalFinishPhase();
        setPlayerSprite("victory");
    };

    const originalShowMap = showMap;
    showMap = function () {
        scene.style.display = "none";
        originalShowMap();
    };

    const originalBackToMenu = backToMenu;
    backToMenu = function () {
        scene.style.display = "none";
        originalBackToMenu();
    };

    let previousSignature = "";
    let animationFrame = 0;

    function animatePlayer() {
        const playing =
            mapScreen.style.display === "none" &&
            mainMenu.style.display === "none" &&
            leaderboardScreen.style.display !== "flex" &&
            challengeModal.style.display !== "flex" &&
            resultModal.style.display !== "flex";

        if (playing) {
            const movingRight = keys["d"] || keys["arrowright"];
            const movingLeft = keys["a"] || keys["arrowleft"];
            const movingUp = keys["w"] || keys["arrowup"];
            const movingDown = keys["s"] || keys["arrowdown"];
            const moving = movingRight || movingLeft || movingUp || movingDown;

            let sprite = "idle";

            if (movingUp && !movingLeft && !movingRight) {
                sprite = "back";
            } else if (moving) {
                const cycle = ["walk1", "walk2", "run1", "run2"];
                sprite = cycle[Math.floor(animationFrame / 10) % cycle.length];
            } else if (near) {
                sprite = "alert";
            }

            const signature = `${sprite}:${movingLeft ? "L" : "R"}`;
            if (signature !== previousSignature) {
                setPlayerSprite(sprite, movingLeft);
                previousSignature = signature;
            }

            animationFrame++;
        }

        requestAnimationFrame(animatePlayer);
    }

    renderMap();
    requestAnimationFrame(animatePlayer);
})();