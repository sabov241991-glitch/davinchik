document.addEventListener('DOMContentLoaded', function() {
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const messagesContainer = document.getElementById('messages');
    const room = document.getElementById('room').value;

    // Функция для загрузки сообщений
    function loadMessages() {
        fetch(`/get_messages/${room}`)
            .then(response => response.json())
            .then(messages => {
                displayMessages(messages);
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            })
            .catch(error => console.error('Error:', error));
    }

    // Функция для отображения сообщений
    function displayMessages(messages) {
        const currentUser = sessionStorage.getItem('username') || '';
        messagesContainer.innerHTML = '';
        
        messages.forEach(msg => {
            const messageDiv = document.createElement('div');
            messageDiv.style.marginBottom = '10px';
            messageDiv.style.padding = '5px';
            messageDiv.style.borderBottom = '1px dotted #ccc';
            
            // Проверяем, является ли сообщение действием (/me)
            let messageContent = msg.message;
            if (msg.message.startsWith('*') && msg.message.endsWith('*')) {
                messageDiv.style.fontStyle = 'italic';
                messageDiv.style.color = '#666666';
                messageContent = msg.message;
            } else if (msg.message.startsWith('/w ')) {
                messageDiv.style.background = '#FFF0F0';
                messageDiv.style.borderLeft = '3px solid #FF3366';
            }
            
            messageDiv.innerHTML = `
                <font size="2">
                    <b>${msg.username}:</b> ${messageContent}
                    <font color="#666666" size="1">(${msg.timestamp})</font>
                </font>
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
            formData.append('room', room);
            
            fetch('/send_message', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    messageInput.value = '';
                    loadMessages();
                } else if (data.status === 'private') {
                    messageInput.value = '';
                    alert(`Приватное сообщение отправлено пользователю ${data.to}`);
                }
            })
            .catch(error => console.error('Error:', error));
        }
    }

    // Обработчики событий
    sendButton.addEventListener('click', sendMessage);
    
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Загрузка сообщений при загрузке страницы
    loadMessages();
    
    // Обновление сообщений каждые 3 секунды
    setInterval(loadMessages, 3000);
    
    // Обновление онлайн пользователей каждые 10 секунд
    setInterval(() => {
        fetch('/get_online_users')
            .then(response => response.json())
            .then(users => {
                // Здесь можно обновить список онлайн пользователей
                console.log('Online users:', users);
            })
            .catch(error => console.error('Error:', error));
    }, 10000);

    // Сохраняем имя пользователя в sessionStorage
    const usernameElement = document.querySelector('font b');
    if (usernameElement) {
        sessionStorage.setItem('username', usernameElement.textContent);
    }
});

// Функция для отправки приватных сообщений (на странице приватных сообщений)
if (document.getElementById('pm-send')) {
    document.getElementById('pm-send').addEventListener('click', function() {
        const toUser = document.getElementById('pm-to').value.trim();
        const message = document.getElementById('pm-message').value.trim();
        
        if (toUser && message) {
            const formData = new FormData();
            formData.append('to_user', toUser);
            formData.append('message', message);
            
            fetch('/send_private', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Сообщение отправлено!');
                    document.getElementById('pm-to').value = '';
                    document.getElementById('pm-message').value = '';
                }
            })
            .catch(error => console.error('Error:', error));
        } else {
            alert('Заполните все поля!');
        }
    });
                  }
