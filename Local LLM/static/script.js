const input = document.getElementById("user-input");
const chatBox = document.getElementById("chat-box");
const sendBtn = document.getElementById("send-btn");

sendBtn.addEventListener("click", sendMessage);
input.addEventListener("keypress", (e) => {
    if (e.key === "Enter") sendMessage();
});

async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    appendMessage("user", message);
    input.value = "";

    // Show typing indicator
    const loader = appendLoader();

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();

        // Remove loader before showing bot reply
        loader.remove();

        appendMessage("bot", data.reply);
    } catch (error) {
        loader.remove();
        appendMessage("bot", "⚠️ Sorry, something went wrong. Please try again.");
        console.error(error);
    }
}

function appendMessage(sender, text) {
    const msg = document.createElement("div");
    msg.classList.add("message", sender, "fade-in");
    msg.textContent = text;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Loader (typing indicator)
function appendLoader() {
    const loader = document.createElement("div");
    loader.classList.add("message", "bot", "loader-bubble");
    loader.innerHTML = `
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
    `;
    chatBox.appendChild(loader);
    chatBox.scrollTop = chatBox.scrollHeight;
    return loader;
}
