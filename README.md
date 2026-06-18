# Чат-бот МИЗО РБ с LLM-интеграцией
## Архитектура
```
Пользователь (VK)
      │  текстовый вопрос
      ▼
IntentClassifier ──► LLM
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
