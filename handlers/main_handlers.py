from keyboards import get_main_keyboard, get_categories_keyboard


def register_main_handlers(bot, db, ilogger=None):

    @bot.on.message(text=["/start", "Начать", "Старт", "Привет", "начать", "привет"])
    async def start(message):
        await message.answer(
            "Здравствуйте! Я интеллектуальный помощник МИЗО РБ.\n\n"
            "Вы можете:\n"
            "• Задать вопрос в свободной форме — ИИ найдёт ответ\n"
            "• Использовать меню для быстрой навигации\n\n"
            "Например: «Какие документы нужны участнику СВО для получения земли?»",
            keyboard=get_main_keyboard(),
        )

    @bot.on.message(payload={"cmd": "main"})
    async def main_menu(message):
        await message.answer(
            "Главное меню. Выберите раздел или задайте вопрос:",
            keyboard=get_main_keyboard(),
        )

    @bot.on.message(payload={"cmd": "categories"})
    async def categories(message):
        await message.answer(
            "Выберите категорию граждан:",
            keyboard=get_categories_keyboard(),
        )

    @bot.on.message(payload={"cmd": "stats"})
    async def stats(message):
        """Статистика для администратора (только при наличии ilogger)."""
        if ilogger is None:
            return
        data = ilogger.get_stats()
        text = (
            "📊 Статистика чат-бота\n\n"
            f"Всего обращений:  {data.get('total', 0)}\n"
            f"Среднее время LLM: {data.get('avg_ms', 0)} мс\n"
            f"Средняя уверенность: {data.get('avg_confidence', 0)}\n"
            f"Средняя оценка: {data.get('avg_rating', 0)} ⭐\n\n"
            f"По категориям:\n"
            f"  СВО:           {data.get('svo', 0)}\n"
            f"  Многодетные:   {data.get('large_family', 0)}\n"
            f"  Законы:        {data.get('laws', 0)}\n"
            f"  Не определено: {data.get('unknown', 0)}\n"
        )
        await message.answer(text, keyboard=get_main_keyboard())
