document.addEventListener('DOMContentLoaded', () => {
    const HOST = "127.0.0.1";
    const PORT = 65432;

    const URL = ""

    let finalPOST_URL;

    const ENDPOINT_POST = "send_mouse_pos"
    const ENDPOINT_GET = "get_mouse_data"

    if (URL && URL.trim() !== "") {
        // URL is NOT empty → use URL + endpoint
        finalPOST_URL = `${URL}/${ENDPOINT_POST}`;
        finalGET_URL = `${URL}/${ENDPOINT_GET}`;
    } else {
        // URL is empty → use the HOST:PORT format
        finalPOST_URL = `http://${HOST}:${PORT}/${ENDPOINT_POST}`;
        finalGET_URL = `http://${HOST}:${PORT}/${ENDPOINT_GET}`;
    }

    console.log(finalPOST_URL)
    console.log(finalGET_URL)


    const square = document.getElementById('square');
    if (!square) return;

    let lastSent = 0;        // timestamp of last POST
    const delay = 100;       // minimum ms between requests

    // Move the square and send POST with throttling
    document.addEventListener('mousemove', e => {
        const mouseX = e.clientX;
        const mouseY = e.clientY;

        square.style.left = mouseX + 'px';
        square.style.top = mouseY + 'px';

        const now = Date.now();
        if (now - lastSent >= delay) {
            lastSent = now;
            const body = `x=${mouseX}&y=${mouseY}&session_id=${getSessionId()}`;
            console.log("POST SEND")

            let result;

            fetch(finalPOST_URL, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "Bypass-Tunnel-Reminder": "true"
                },
                credentials: "include",
                body: body
            }).then(response => response.json())
            .then(data => {
                updateCubes(data)
                console.log(data)
            })
            .catch(err => console.error("POST failed:", err));

        }
    });
});

const cubes = {};

function updateCubes(data) {
    for (const id in data) {
        const { x, y } = data[id];

        // If cube doesn't exist for this ID, create it
        if (!cubes[id]) {
            const cube = document.createElement('div');
            cube.classList.add('cube');

            // Optional: assign random color
            cube.style.backgroundColor = `hsl(${Math.random() * 360}, 70%, 50%)`;

            document.body.appendChild(cube);
            cubes[id] = cube;
        }

        // Update cube position
        cubes[id].style.transform = `translate(${x}px, ${y}px) translate(-50%, -50%)`;
    }
}

function getSessionId() {
    return document.cookie
        .split("; ")
        .find(row => row.startsWith("session_id="))
        ?.split("=")[1] || "-1";
}
