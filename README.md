# 🤖 Crypto Telegram Bot with Heleket Integration

Telegram-бот с оплатой криптовалютой через [Heleket](https://heleket.com/?utm_source=youtube&utm_medium=blogger&utm_campaign=shcoder001).  
Позволяет пользователю покупать подписку, проверять оплату и получать доступ к премиум-функциям.

## 🔗 Ссылки

- 🧠 Проект на GitHub: [ShcoderDev/crypto-telegrambot-heleket](https://github.com/ShcoderDev/crypto-telegrambot-heleket)
- 💰 Платёжный провайдер: [Heleket.com](https://heleket.com/?utm_source=youtube&utm_medium=blogger&utm_campaign=shcoder001)

---

## ⚙️ Установка и запуск

### 📥 1. Клонирование репозитория

```bash
git clone https://github.com/ShcoderDev/crypto-telegrambot-heleket.git
cd crypto-telegrambot-heleket
````

---

### 📦 2. Установка зависимостей

Убедитесь, что у вас установлен **Python 3.10+**, затем установите зависимости:

```bash
pip install -r requirements.txt
```

---

### 🔐 3. Настройка конфигурации

Создайте файл `config.py` в корне проекта и вставьте в него свои ключи:

```python
# config.py

BOT_TOKEN = "your_telegram_bot_token"
MERCHANT_UUID = "your_merchant_uuid"
API_KEY = "your_heleket_api_secret"
```

📌 Ключи можно получить после регистрации на [heleket.com](https://heleket.com/?utm_source=youtube&utm_medium=blogger&utm_campaign=shcoder001)

---

### 🚀 4. Запуск бота

```bash
python main.py
```

---

## Возможности

* `/start` — запуск бота и приветствие
* Купить подписку — создаёт крипто-счёт через Heleket
* Проверка оплаты — подтверждение транзакции и активация подписки
* Личный кабинет — показывает дату окончания подписки

---

## Как работает

1. Пользователь нажимает **Купить подписку**
2. Бот создаёт счёт в криптовалюте через API Heleket
3. UUID счёта сохраняется в базу данных
4. Пользователь оплачивает и нажимает **Проверить оплату**
5. При успешной оплате активируется подписка сроком на 30 дней
