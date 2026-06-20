# Чат-бот МИЗО РБ с LLM-интеграцией

## Архитектура

```
Пользователь (VK)
      │  текстовый вопрос
      ▼
IntentClassifier ──► LLM (GigaChat / YandexGPT / OpenRouter / Ollama)
      │  category + subtopic + measure_id
      ▼
AnswerGenerator
      ├── _retrieve_context() ──► PostgreSQL (RAG)
      │         svo_measures / large_family / laws_parts / common
      └── LLM.complete(system, context + question)
                │  сгенерированный ответ
                ▼
      ContextManager (история диалога)
      InteractionLogger (логи + оценки пользователей)
                │
                ▼
      Пользователь получает ответ + кнопки + запрос оценки
```

## Быстрый старт

```bash
# 1. Установить зависимости
pip install -r requirements.txt

# 2. Скопировать конфиг и заполнить
cp .env.example .env
nano .env          # указать LLM_BACKEND и ключ

# 3. Запустить
python bot.py
```

## Структура проекта

```
mizo_bot_ai/
├── bot.py                  ← точка входа
├── .env.example            ← шаблон конфига
├── requirements.txt
├── ai/
│   ├── llm_provider.py     ← универсальный LLM-клиент
│   ├── intent_classifier.py← классификация намерений
│   ├── answer_generator.py ← RAG + генерация ответов
│   ├── context_manager.py  ← история диалога
│   └── interaction_logger.py← логирование + оценки
├── handlers/
│   ├── ai_handler.py       ← catch-all текстовый handler
│   ├── main_handlers.py
│   ├── svo_handlers.py     ← статические (кнопки)
│   ├── large_handlers.py
│   ├── laws_handlers.py
│   └── common_handlers.py
├── database/
│   └── db.py
└── keyboards.py
```

## Таблица логов (создаётся автоматически)

```sql
interaction_logs (
    id, user_id, user_msg,
    category, subtopic, measure_id,
    confidence,           -- уверенность классификатора
    bot_answer,
    data_source,          -- откуда взяты данные
    llm_ms,               -- время ответа LLM в мс
    rating,               -- оценка пользователя 1-5
    created_at
)
```
