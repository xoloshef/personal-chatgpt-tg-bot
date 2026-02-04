# personal-chatgpt-tg-bot

Многофункциональный Telegram-бот с поддержкой LLM (OpenAI / OpenAI-compatible API), плагинов и транскрибации аудио из голосового сообщения.  
Создано для личного использования.

Рекомендованная версия  Python 3.12

 Файл `.env` не должен попадать в git

 Для работы с API OpenAI ChatGPT необходим депозит 5$ в лк OpenAI Platform (см пункт 1.2 Получите API ключ от ChatGPT)

## Возможности

### Чат
- Контекстные диалоги (хранится история сообщений (MAX_HISTORY_SIZE=5))
- Сокращение длинных диалогов
- Streaming-ответы (сообщение редактируется по мере генерации)

### Плагины (bot/plugins)
Бот умеет вызывать внешние инструменты через OpenAI function calling:

- Веб-поиск и поиск изображений (DuckDuckGo)
- Транскрибация видео YouTube (OpenAI Whisper)
- Транскрибация  голосового сообщения Telegram (OpenAI Whisper)
- Математика (WolframAlpha)
- Погода (Open-Meteo)
- Время и таймзоны
- Курсы Криптовалют
- Переводы (DeepL)

---
### Работа с аудио
- Поддержка **voice / audio / video / video note**
- Конвертация через `ffmpeg`
- Транскрибация через OpenAI Whisper
- Опциональный ответ LLM по тексту транскрипции
- Подсчёт токенов и секунд транскрибации

---
### Фукционал

- Команда (`/stats`) для отслеживания трат токенов и отслеживания баланса OpenAI
- Подсчёт токенов и секунд транскрибации
- Логи использования сохраняются в `usage_logs/`

---

## Структура проекта

```text
.
├── bot/
│   ├── main.py              # Точка входа
│   ├── telegram_bot.py      # Telegram handlers и логика
│   ├── openai_helper.py     # Работа с LLM и контекстом
│   ├── plugin_manager.py    # Загрузка и вызов плагинов
│   ├── usage_tracker.py     # Учёт лимитов и расходов
│   ├── utils.py             # Вспомогательные функции
│   └── plugins/             # Плагины
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── requirements-minimal.txt
├── translations.json
├── .env.example
└── usage_logs/
```

---

## Старт - Start 

### 1.1 Получите API ключ для telegram бота

Написать t.me/BotFather @BotFather
1)  `/start`
2)  `/newbot`
	Cледуете предлагаемой инструкции @BotFather
3) Задайте отображаемое имя бота (Пример: `ChatGPT_bot`)
4) Задайте username (Пример: `ChatGPT_123456_bot`)
После успешного создания:
5) Общение с ботом (Пример t.me / `ChatGPT_123456_bot`)
6) Скопируйте API ключ (После `Use this token to access the HTTP API:`
7) Скопируйте API ключ в `.env.example.md`
	Местонахождение (`/personal-chatgpt-tg-bot/.env.example.md`)
	Найти элемент 
	```markdown
	4 # Your Telegram bot token obtained using @BotFather
	5 TELEGRAM_BOT_TOKEN=XXX
	```
8) Заменить значение `YOUR_OPENAI_API_KEY_HERE` на скопированный API ключ из телеграм  (пункт 6)
	Пример :
	```markdown
	4 # Your Telegram bot token obtained using @BotFather
	5 TELEGRAM_BOT_TOKEN='87654321:AAAA...'
	```

### 1.2 Получите API ключ от ChatGPT 

1) Войдите в учетную запись openai.com
2) Перейти openai.com --> platform -- > Боковое меню, раздел Manage --> API keys
	https://platform.openai.com/api-keys
3) Перейти в меню `Create new secret key`
4) Создать `Create secret key`
5) Скопируйте API ключ в `.env.example.md`
	Местонахождение (`/personal-chatgpt-tg-bot/.env.example.md`)
	Найти элемент 
	```markdown
	1 # Your OpenAI API key
	2 OPENAI_API_KEY=YOUR_OPENAI_API_KEY_HERE
	```
6) Заменить значение `YOUR_OPENAI_API_KEY_HERE` на скопированный API ключ из телеграм  (пункт 6)
	Пример :
	```markdown
	1 # Your OpenAI API key
	2 OPENAI_API_KEY='AAAA...'
	```

####  1.3 Настройка конфигурационного файла `.env`

**.env не должен попадать в git**

1) Рекомендуеммые параметры `.env.example.md`

```markdown
OPENAI_API_KEY='XXX' # см пункт 1.2 API ключ от ChatGPT
TELEGRAM_BOT_TOKEN='XXX' # см пункт 1.1 API ключ для telegram бота
ADMIN_USER_IDS=XXX # ваш id telegram акаунта пример 11...
ALLOWED_TELEGRAM_USER_IDS=XXX  # ваш id telegram акаунта пример 11...

MAX_HISTORY_SIZE=5
BOT_LANGUAGE=ru
VISION_MODEL="gpt-4o"
OPENAI_MODEL=gpt-4o
```

2) Переименовать файл `.env.example.md` в `.env`

### 2 Настройка зависимостей - Старт - Запуск

Рекомендованная версия Python 3.12

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python bot/main.py
```
