document.addEventListener('DOMContentLoaded', function() {
    initializeCounters();
    setupEventListeners();
    startCounterUpdates();
});

function initializeCounters() {
    const counters = {
        'onlineCount': 1,
        'newUsers': 0,
        'birthdays': 41,
        'totalRegistrations': 19572,
        'totalMen': 11987,
        'totalWomen': 7585,
        'totalPartners': 7,
        'dailyVisitors': 44
    };
    
    for (const [id, value] of Object.entries(counters)) {
        const element = document.getElementById(id);
        if (element) {
            element.textContent = value.toLocaleString();
        }
    }
}

function setupEventListeners() {
    const loginBtn = document.getElementById('loginBtn');
    if (loginBtn) {
        loginBtn.addEventListener('click', handleLogin);
    }
    
    const rememberCheckbox = document.getElementById('remember');
    const translitCheckbox = document.getElementById('translit');
    
    if (rememberCheckbox) {
        rememberCheckbox.addEventListener('change', function() {
            if (this.checked) {
                saveUserPreferences();
            }
        });
    }
    
    if (translitCheckbox) {
        translitCheckbox.addEventListener('change', function() {
            toggleTranslit(this.checked);
        });
    }
    
    loadUserPreferences();
}

function handleLogin(event) {
    event.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    if (!username || !password) {
        alert('Пожалуйста, заполните все поля');
        return;
    }
    
    simulateLogin(username, password);
}

function simulateLogin(username, password) {
    const loginBtn = document.getElementById('loginBtn');
    const originalText = loginBtn.textContent;
    loginBtn.textContent = 'Вход...';
    loginBtn.disabled = true;
    
    setTimeout(() => {
        const success = Math.random() > 0.2;
        
        if (success) {
            alert(`Добро пожаловать, ${username}!`);
            updateOnlineCount(1);
        } else {
            alert('Неверный логин или пароль');
        }
        
        loginBtn.textContent = originalText;
        loginBtn.disabled = false;
    }, 1500);
}

function updateOnlineCount(change) {
    const onlineElement = document.getElementById('onlineCount');
    if (onlineElement) {
        let currentCount = parseInt(onlineElement.textContent.replace(/,/g, '')) || 0;
        currentCount += change;
        onlineElement.textContent = currentCount.toLocaleString();
    }
}

function toggleTranslit(enabled) {
    const usernameInput = document.getElementById('username');
    if (enabled) {
        usernameInput.addEventListener('input', handleTranslit);
    } else {
        usernameInput.removeEventListener('input', handleTranslit);
    }
}

function handleTranslit(event) {
    const input = event.target;
    const value = input.value;
    
    const translitMap = {
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
        'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
        'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n',
        'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
        'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch',
        'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '',
        'э': 'e', 'ю': 'yu', 'я': 'ya'
    };
    
    let newValue = '';
    for (let char of value.toLowerCase()) {
        newValue += translitMap[char] || char;
    }
    
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
            
            if (preferences.translit) {
                toggleTranslit(true);
            }
        } catch (e) {
            console.error('Error loading preferences:', e);
        }
    }
}

function startCounterUpdates() {
    setInterval(() => {
        const onlineElement = document.getElementById('onlineCount');
        if (onlineElement) {
            const current = parseInt(onlineElement.textContent.replace(/,/g, '')) || 0;
            const change = Math.floor(Math.random() * 3) - 1;
            const newCount = Math.max(1, current + change);
            onlineElement.textContent = newCount.toLocaleString();
        }
    }, 30000);
    
    setInterval(() => {
        updateOtherCounters();
    }, 120000);
}

function updateOtherCounters() {
    const counters = {
        'newUsers': {min: 0, max: 5},
        'dailyVisitors': {min: 40, max: 60}
    };
    
    for (const [id, range] of Object.entries(counters)) {
        const element = document.getElementById(id);
        if (element) {
            const current = parseInt(element.textContent.replace(/,/g, '')) || 0;
            const change = Math.floor(Math.random() * (range.max - range.min + 1)) + range.min;
            element.textContent = change.toLocaleString();
        }
    }
              }
