function appendMessage(message, isUser) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;

    // Regular expression to detect URLs
    const urlRegex = /(https?:\/\/[^\s]+)/g;
    messageDiv.innerHTML = message.replace(urlRegex, '<a href="$1" target="_blank">$1</a>');

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function appendTypingBubble() {
    const chatMessages = document.getElementById('chat-messages');
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-bubble';
    typingDiv.textContent = 'Typing...';
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return typingDiv; // Return the typing bubble element so we can remove it later
}

async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const message = userInput.value.trim();
    
    if (message) {
        appendMessage(message, true); // Append the user's message
        userInput.value = '';

        // Add a typing bubble
        const typingBubble = appendTypingBubble();
        
        try {
            const response = await fetch('/get_response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `user_input=${encodeURIComponent(message)}`
            });
            
            const data = await response.json();

            // Remove the typing bubble
            typingBubble.remove();

            // Append the bot's response
            appendMessage(data.bot_response, false);
        } catch (error) {
            console.error('Error:', error);

            // Remove the typing bubble
            typingBubble.remove();

            // Append an error message
            appendMessage("Sorry, I'm having trouble responding right now.", false);
        }
    }
}

// Handle Enter key
document.getElementById('user-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});