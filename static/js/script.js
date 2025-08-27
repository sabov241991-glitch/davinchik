// Глобальные переменные для счетчиков
let chatStats = {
    online: 1, // Минимум 1 (админ)
    newUsers: 0,
    birthdays: 0,
    totalRegistrations: 0,
    totalMen: 0,
    totalWomen: 0,
    totalPartners: 0,
    dailyVisitors: 0
};

document.addEventListener('DOMContentLoaded', function() {
    initializePage();
    setupEventListeners();
    loadFromStorage();
    updateDisplay();
});

function initializePage() {
    updateDateTime();
    setupDailyReset();
}

function updateDateTime() {
    const now = new Date();
    
    const timeElement = document.getElementById('currentTime');
    const dateElement = document.getElementById('currentDate');
    const dayElement = document.getElementById('currentDay');
    
    if (timeElement) timeElement.textContent = now.toLocaleTimeString('ru-RU');
    if (dateElement) {
        const options = { day: 'numeric', month: 'long', year: 'numeric' };
        dateElement.textContent = now.toLocaleDateString('ru-RU', options);
    }
    if (dayElement) {
        const days = ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'];
        dayElement.textContent = days[now.getDay()];
    }
}

function setupEventListeners() {
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) loginBtn.addEventListener('click', handleLogin);
    
    const rememberCheckbox = document.getElementById('remember');
    const translitCheckbox = document.getElementById('translit');
    
    if (rememberCheckbox) {
        rememberCheckbox.addEventListener('change', function() {
            if (this.checked) saveUserPreferences();
        });
    }
    
    if (translitCheckbox) {
        translitCheckbox.addEventListener('change', function() {
            toggleTranslit(this.checked);
        });
    }
    
    setInterval(updateDateTime, 1000);
}

function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value.trim();
    const password = document.getElementById('password').value.trim();
    
    if (!username || !password) {
        showMessage('Пожалуйста, заполните все поля', 'error');
        return;
    }
    
    const isNewUser = checkIfNewUser(username);
    simulateLogin(username, password, isNewUser);
}

function checkIfNewUser(username) {
    const registeredUsers = JSON.parse(localStorage.getItem('registeredUsers') || '[]');
    return !registeredUsers.includes(username.toLowerCase());
}

function simulateLogin(username, password, isNewUser) {
    const loginBtn = document.getElementById('loginBtn');
    const originalText = loginBtn.textContent;
    
    loginBtn.textContent = 'Вход...';
    loginBtn.disabled = true;
    
    setTimeout(() => {
        const success = Math.random() > 0.1;
        
        if (success) {
            if (isNewUser) registerNewUser(username);
            
            chatStats.online++;
            chatStats.dailyVisitors++;
            
            showMessage(`Добро пожаловать, ${username}!`, 'success');
            updateDisplay();
            saveToStorage();
        } else {
            showMessage('Неверный логин или пароль', 'error');
        }
        
        loginBtn.textContent = originalText;
        loginBtn.disabled = false;
    }, 2000);
}

function registerNewUser(username) {
    const isMale = Math.random() > 0.5;
    
    chatStats.totalRegistrations++;
    chatStats.newUsers++;
    isMale ? chatStats.totalMen++ : chatStats.totalWomen++;
    
    const registeredUsers = JSON.parse(localStorage.getItem('registeredUsers') || '[]');
    registeredUsers.push(username.toLowerCase());
    localStorage.setItem('registeredUsers', JSON.stringify(registeredUsers));
    
    if (Math.random() < 0.01) chatStats.birthdays++;
}

function updateDisplay() {
    document.getElementById('onlineCount').textContent = chatStats.online;
    document.getElementById('newUsers').textContent = chatStats.newUsers;
    document.getElementById('birthdays').textContent = chatStats.birthdays;
    document.getElementById('totalRegistrations').textContent = formatNumber(chatStats.totalRegistrations);
    document.getElementById('totalMen').textContent = formatNumber(chatStats.totalMen);
    document.getElementById('totalWomen').textContent = formatNumber(chatStats.totalWomen);
    document.getElementById('totalPartners').textContent = chatStats.totalPartners;
    document.getElementById('dailyVisitors').textContent = chatStats.dailyVisitors;
}

function formatNumber(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, " ");
}

function showMessage(text, type) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;
    messageDiv.style.cssText = `
        position: fixed; top: 20px; left: 50%; transform: translateX(-50%);
        padding: 15px 25px; background: ${type === 'success' ? '#4caf50' : '#f44336'};
        color: white; border-radius: 8px; z-index: 1000; font-weight: bold;
    `;
    
    document.body.appendChild(messageDiv);
    setTimeout(() => messageDiv.remove(), 3000);
}

function toggleTranslit(enabled) {
    const usernameInput = document.getElementById('username');
    enabled ? usernameInput.addEventListener('input', handleTranslit) 
            : usernameInput.removeEventListener('input', handleTranslit);
}

function handleTranslit(event) {
    const input = event.target;
    const value = input.value;
    const translitMap = {
        'а':'a','б':'b','в':'v','г':'g','д':'d','е':'e','ё':'yo','ж':'zh','з':'z',
        'и':'i','й':'y','к':'k','л':'l','м':'m','н':'n','о':'o','п':'p','р':'r',
        'с':'s','т':'t','у':'u','ф':'f','х':'h','ц':'ts','ч':'ch','ш':'sh','щ':'sch',
        'ъ':'','ы':'y','ь':'','э':'e','ю':'yu','я':'ya'
    };
    
    let newValue = '';
    for (let char of value.toLowerCase()) newValue += translitMap[char] || char;
    input.value = newValue;
}

function saveUserPreferences() {
    const preferences = {
        username: document.getElementById('username').value,
        translit: document.getElementById('translit').checked,
        remember: document.getElementById('remember').checked
    };
    localStorage.setItem('chatPreferences', JSON.stringify(preferences));
}

function loadUserPreferences() {
    const saved = localStorage.getItem('chatPreferences');
    if (saved) {
        try {
            const preferences = JSON.parse(saved);
            if (preferences.remember && preferences.username) {
                document.getElementById('username').value = preferences.username;
            }
            document.getElementById('translit').checked = preferences.translit || false;
            document.getElementById('remember').checked = preferences.remember || false;
            if (preferences.translit) toggleTranslit(true);
        } catch (e) {
            console.error('Error loading preferences:', e);
        }
    }
}

function saveToStorage() {
    localStorage.setItem('chatStats', JSON.stringify(chatStats));
}

function loadFromStorage() {
    const saved = localStorage.getItem('chatStats');
    if (saved) {
        try {
            const loadedStats = JSON.parse(saved);
            // Сохраняем только если данные не повреждены
            if (loadedStats && typeof loadedStats === 'object') {
                chatStats = { ...chatStats, ...loadedStats };
            }
        } catch (e) {
            console.error('Error loading stats:', e);
        }
    }
    updateDisplay();
}

function setupDailyReset() {
    const lastReset = localStorage.getItem('lastReset');
    const today = new Date().toDateString();
    
    if (lastReset !== today) {
        chatStats.newUsers = 0;
        chatStats.dailyVisitors = 0;
        chatStats.birthdays = 0;
        localStorage.setItem('lastReset', today);
        saveToStorage();
        updateDisplay();
    }
      }
