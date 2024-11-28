let messageHistory = [];

function showSpinner() {
    document.getElementById('spinner').style.display = 'flex';
}

function hideSpinner() {
    document.getElementById('spinner').style.display = 'none';
}

function saveToLocalStorage(message, isUser) {
    messageHistory.push({ message, isUser });
    localStorage.setItem('chatHistory', JSON.stringify(messageHistory));
}

function loadFromLocalStorage() {
    const saved = localStorage.getItem('chatHistory');
    if (saved) {
        messageHistory = JSON.parse(saved);
        messageHistory.forEach(msg => appendMessage(msg.message, msg.isUser));
    }
}

function appendMessage(message, isUser) {
    const messagesDiv = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'assistant-message'}`;
    
    const content = document.createElement('div');
    content.className = 'content';
    content.innerHTML = isUser ? message : marked.parse(message);
    messageDiv.appendChild(content);
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
    
    saveToLocalStorage(message, isUser);
}

async function sendMessage() {
    const input = document.getElementById('user-input');
    const message = input.value.trim();
    
    if (!message) return;
    
    input.value = '';
    appendMessage(message, true);
    
    try {
        showSpinner();
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.error) {
            appendMessage(`Error: ${data.error}`, false);
        } else {
            appendMessage(data.answer, false);
            
            if (data.sources && data.sources.length > 0) {
                const sourcesDiv = document.createElement('div');
                sourcesDiv.className = 'sources';
                sourcesDiv.innerHTML = '<strong>Sources:</strong><br>' + 
                    data.sources.map(s => `- ${s.source} (${s.directory})`).join('<br>');
                document.querySelector('.message:last-child').appendChild(sourcesDiv);
            }
        }
    } catch (error) {
        console.error('Error:', error);
        appendMessage(`Error: ${error.message}`, false);
    } finally {
        hideSpinner();
    }
}

function handleKeyPress(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
        // Reset textarea height only after sending
        setTimeout(() => {
            const textarea = document.getElementById('user-input');
            textarea.style.height = 'auto';
            textarea.style.height = textarea.scrollHeight + 'px';
        }, 0);
    }
}

function autoResizeTextarea() {
    const textarea = document.getElementById('user-input');
    // Reset height to auto to get the correct scrollHeight
    textarea.style.height = 'auto';
    // Set new height based on scrollHeight
    textarea.style.height = textarea.scrollHeight + 'px';
}

document.addEventListener('DOMContentLoaded', () => {
    loadFromLocalStorage();
    
    const textarea = document.getElementById('user-input');
    textarea.addEventListener('input', autoResizeTextarea);
    // Also handle paste events
    textarea.addEventListener('paste', () => {
        setTimeout(autoResizeTextarea, 0);
    });
});

async function startNewChat() {
    try {
        const response = await fetch('/api/new-chat', {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        // Clear message history
        messageHistory = [];
        localStorage.removeItem('chatHistory');
        
        // Clear chat messages
        const messagesDiv = document.getElementById('chat-messages');
        messagesDiv.innerHTML = '';
        
        // Show notification
        appendMessage("Starting new conversation...", false);
        
    } catch (error) {
        console.error('Error:', error);
        appendMessage(`Error: ${error.message}`, false);
    }
}