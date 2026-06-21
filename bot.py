import os
import logging
import asyncio
from dotenv import load_dotenv
from vkbottle.bot import Bot

from database import Database
from ai import (
    get_llm_provider,
    IntentClassifier,
    AnswerGenerator,
    ContextManager,
    InteractionLogger,
)
from handlers import (
    register_main_handlers,
    register_svo_handlers,
    register_large_handlers,
    register_laws_handlers,
    register_common_handlers,
    register_ai_handler,
)

# Конфигурация

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

VK_TOKEN = os.getenv(
    "VK_TOKEN",
    "vk1.a.RqANJS6I8X6XGyNBhGafndK-PkDC1gKP0KQJGARLa3H1_AX8dX4_Yzn2bMorUr_dhEHJooNWcc529Ewr40u7EImUgtBMV5x4_uULu0Aky_w2_9CCqVoUhxgLbfnvX_EWUVa5NSPC49-y_Ia90sC7J9R6Blg1XG-kdApPD3GHhEnQzldxOFVzIboL2sWJf2amwzBZY1QKUcpyVjxiQhBU4Q"
)

# Инициализация

bot = Bot(token=VK_TOKEN)

# База данных
db = Database(
    host="aws-1-eu-central-1.pooler.supabase.com",
    port=5432,
    database="postgres",
    user="postgres.gfczyycvyyqmdcqyfmxq",
    password="Chased_Away1",
)
db.connect()
logger.info("Подключение к PostgreSQL установлено")

# AI-компоненты
llm        = get_llm_provider()
classifier = IntentClassifier(llm)
ctx_mgr    = ContextManager()
ilogger    = InteractionLogger(db)
generator  = AnswerGenerator(llm, db)

# Регистрация handlers

register_main_handlers(bot, db, ilogger)
register_svo_handlers(bot, db)
register_large_handlers(bot, db)
register_laws_handlers(bot, db)
register_common_handlers(bot, db)

# AI catch-all — обрабатывает любой свободный текст
register_ai_handler(bot, db, classifier, generator, ctx_mgr, ilogger)

logger.info(f"LLM-провайдер: {os.getenv('LLM_BACKEND', 'openrouter')}")


# Фоновая задача: очистка контекстов

async def cleanup_task():
    while True:
        await asyncio.sleep(600)  # каждые 10 минут
        removed = ctx_mgr.cleanup_expired()
        if removed:
            logger.info(f"Очищено {removed} устаревших контекстов")


# Запуск
if __name__ == "__main__":
    logger.info("Бот запускается...")
    loop = asyncio.get_event_loop()
    loop.create_task(cleanup_task())
    bot.run_forever()
