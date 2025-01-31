document.addEventListener("DOMContentLoaded", function () {
    const chatMessages = document.getElementById("chat-messages");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");

    
    sendBtn.addEventListener("click", async () => {
        const message = userInput.value.trim();
        if (message) {
            appendMessage("user", message);
            userInput.value = "";

            
            const response = await fetch("/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message }),
            });
            const data = await response.json();
            if (data.response) {
                appendMessage("tutor", data.response);
            } else {
                appendMessage("tutor", "Sorry, something went wrong. Please try again.");
            }
        }
    });

    
    const apiKeyForm = document.getElementById("api-key-form");
    if (apiKeyForm) {
        apiKeyForm.addEventListener("submit", async (e) => {
            e.preventDefault();
            const apiKey = document.getElementById("api-key").value;
            const response = await fetch("/config", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: `api_key=${encodeURIComponent(apiKey)}`,
            });
            const data = await response.json();
            document.getElementById("status-message").textContent = data.message;
        });
    }
});

function appendMessage(sender, message) {
    const chatMessages = document.getElementById("chat-messages");
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", sender);
    messageElement.textContent = message;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}