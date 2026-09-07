const form = document.getElementById("analysisForm");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
        name: document.getElementById("name").value,
        course: document.getElementById("course").value,
        skills: document.getElementById("skills").value,
        interests: document.getElementById("interests").value,
        goal: document.getElementById("goal").value
    };

    const button = form.querySelector("button");
    button.textContent = "Analyzing...";
    button.disabled = true;

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        if (!response.ok) throw new Error("Server error");

        const result = await response.json();

        document.getElementById("career").textContent = result.career;
        document.getElementById("message").textContent = result.message;
        document.getElementById("score").textContent = result.score + "%";

        const missing = document.getElementById("missing");
        missing.innerHTML = "";

        result.missing.forEach(skill => {
            const chip = document.createElement("span");
            chip.className = "chip";
            chip.textContent = skill;
            missing.appendChild(chip);
        });

        const roadmap = document.getElementById("roadmap");
        roadmap.innerHTML = "";
        result.roadmap.forEach(step => {
            const li = document.createElement("li");
            li.textContent = step;
            roadmap.appendChild(li);
        });

        document.getElementById("resultSection").classList.remove("hidden");
        document.getElementById("resultSection").scrollIntoView({ behavior: "smooth" });
    } catch (error) {
        alert("Could not connect to the backend. Make sure Flask is running.");
        console.error(error);
    } finally {
        button.textContent = "Analyze My Career ✨";
        button.disabled = false;
    }
});

async function sendChat() {
    const input = document.getElementById("chatInput");
    const message = input.value.trim();
    if (!message) return;

    addMessage(message, "user");
    input.value = "";

    try {
        const response = await fetch("/api/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const result = await response.json();
        addMessage(result.reply, "bot");
    } catch (error) {
        addMessage("Backend connection failed. Please check that Flask is running.", "bot");
    }
}

function addMessage(text, type) {
    const box = document.getElementById("chatMessages");
    const div = document.createElement("div");
    div.className = type;
    div.textContent = text;
    box.appendChild(div);
    box.scrollTop = box.scrollHeight;
}

document.getElementById("chatInput").addEventListener("keydown", (event) => {
    if (event.key === "Enter") sendChat();
});
