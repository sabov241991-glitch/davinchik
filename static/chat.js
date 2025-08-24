document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const messagesContainer = document.getElementById('messages');
    const logoutButton = document.getElementById('logout-button');

    // Функция для загрузки сообщений
    function loadMessages() {
        fetch('/get_messages')
            .then(response => response.json())
            .then(messages => {
                displayMessages(messages);
                // Автопрокрутка к последнему сообщению
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            })
            .catch(error => console.error('Error loading messages:', error));
    }

    // Функция для отображения сообщений
    function displayMessages(messages) {
        messagesContainer.innerHTML = '';
        const currentUser = document.body.getAttribute('data-username');
        
        messages.forEach(msg => {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${msg.username === currentUser ? 'own' : 'other'}`;
            
            messageDiv.innerHTML = `
                <div class="message-sender">${msg.username}</div>
                <div class="message-text">${msg.message}</div>
                <div class="message-time">${msg.timestamp}</div>
            `;
            
            messagesContainer.appendChild(messageDiv);
        });
    }

    // Функция для отправки сообщения
    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            const formData = new FormData();
            formData.append('message', message);
            
            fetch('/send_message', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    messageInput.value = '';
                    loadMessages();
                }
            })
            .catch(error => console.error('Error sending message:', error));
        }
    }

    // Обработчики событий
    sendButton.addEventListener('click', sendMessage);
    
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    if (logoutButton) {
        logoutButton.addEventListener('click', function() {
            fetch('/logout')
                .then(() => window.location.href = '/')
                .catch(error => console.error('Error logging out:', error));
        });
    }

    // Загрузка сообщений при загрузке страницы
    loadMessages();
    
    // Обновление сообщений каждые 3 секунды
    setInterval(loadMessages, 3000);
});
