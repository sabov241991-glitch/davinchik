import requests
import time
import logging

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

BOT_TOKEN = "8271459301:AAFfJCTj061MFkMgSqbXGp9Vy8JV-XxS5u0"
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

def get_updates(offset=None):
    try:
        url = URL + "getUpdates"
        params = {"timeout": 100, "offset": offset}
        response = requests.get(url, params=params, timeout=10)
        return response.json()
    except:
        return {"result": []}

def send_message(chat_id, text):
    try:
        url = URL + "sendMessage"
        params = {"chat_id": chat_id, "text": text}
        requests.post(url, params=params, timeout=5)
    except:
        pass

def main():
    last_update_id = None
    print("✅ Бот ДАВИНЧИК запущен! Ожидаем сообщения...")
    
    while True:
        try:
            updates = get_updates(last_update_id)
            
            if "result" in updates:
                for update in updates["result"]:
                    last_update_id = update["update_id"] + 1
                    
                    if "message" in update:
                        message = update["message"]
                        chat_id = message["chat"]["id"]
                        text = message.get("text", "")
                        
                        if text == "/start":
                            user = message["from"]
                            name = user.get("first_name", "Друг")
                            send_message(chat_id, 
                                f"🎉 ДАВИНЧИК РАБОТАЕТ!\n"
                                f"Привет, {name}!\n"
                                f"Бот успешно запущен!"
                            )
                            print(f"📩 Отправил приветствие для {name}")
                            
            time.sleep(1)
            
        except Exception as e:
            print(f"⚠️ Ошибка: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
