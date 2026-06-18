"""
ai_handler.py — Обработчик свободных текстовых запросов через LLM.

Регистрирует один handler на любое текстовое сообщение (не payload).
Пайплайн:
  1. classify(message) → Intent
  2. generate(intent)  → answer
  3. log(interaction)
  4. Ответить пользователю + предложить уточняющие кнопки
"""

import time
import logging
from vkbottle.bot import Message as VKMessage

from keyboards import (
    get_main_keyboard,
    get_svo_keyboard,
    get_large_keyboard,
    get_back_keyboard,
)
from ai import (
    IntentClassifier,
    AnswerGenerator,
    ContextManager,
    InteractionLogger,
)

logger = logging.getLogger(__name__)

# Сообщение пока LLM думает
THINKING_MSG = "⏳ Анализирую ваш запрос..."

# Клавиатура с оценкой (показывается после ответа)
RATING_INTRO = "\n\n─────────────────\nОцените ответ:"


def _rating_keyboard(log_id: int):
    """Создать inline-клавиатуру с оценками 1–5."""
    from vkbottle import Keyboard, KeyboardButtonColor, Text
    kb = Keyboard(inline=True)
    for score in (1, 2, 3, 4, 5):
        color = (
            KeyboardButtonColor.NEGATIVE if score <= 2
            else KeyboardButtonColor.POSITIVE if score >= 4
            else KeyboardButtonColor.SECONDARY
        )
        kb.add(
            Text(
                f"{'★' * score}",
                payload={"cmd": "rate", "log_id": log_id, "score": score}
            ),
            color=color,
        )
    return kb


def _suggest_keyboard(category: str):
    """Предложить тематические кнопки после AI-ответа."""
    if category == "svo":
        return get_svo_keyboard()
    if category == "large_family":
        return get_large_keyboard()
    return get_back_keyboard()


def register_ai_handler(bot, db, classifier: IntentClassifier,
                         generator: AnswerGenerator,
                         ctx_manager: ContextManager,
                         ilogger: InteractionLogger):

    @bot.on.message(payload={"cmd": "rate"})
    async def handle_rating(message: VKMessage):
        payload = message.get_payload_json()
        log_id  = payload.get("log_id")
        score   = payload.get("score", 0)
        if log_id and 1 <= score <= 5:
            ilogger.save_rating(log_id, score)
            await message.answer(
                f"Спасибо за оценку! {'⭐' * score}",
                keyboard=get_main_keyboard(),
            )
        else:
            await message.answer("Не удалось сохранить оценку.", keyboard=get_main_keyboard())

    @bot.on.message()
    async def handle_free_text(message: VKMessage):
        """
        Обрабатывает любое текстовое сообщение, не перехваченное другими handlers.
        Этот handler должен регистрироваться ПОСЛЕДНИМ.
        """
        user_id   = message.from_id
        user_text = (message.text or "").strip()

        if not user_text:
            await message.answer(
                "Здравствуйте! Задайте любой вопрос о мерах поддержки граждан.",
                keyboard=get_main_keyboard(),
            )
            return

        # Получаем контекст пользователя
        ctx = ctx_manager.get(user_id)
        ctx.add_message("user", user_text)

        # Сообщение-заглушка пока LLM работает
        await message.answer(THINKING_MSG)

        t0 = time.time()

        # ── 1. Классификация ──────────────────────────────────
        intent = await classifier.classify(user_text)
        ctx.update_from_intent(intent)

        # Если уверенность низкая и тема есть из предыдущего диалога — применяем
        if intent.confidence < 0.5 and ctx.last_category:
            intent.category = ctx.last_category
            if ctx.last_measure and intent.category == "svo":
                intent.measure_id = ctx.last_measure

        # ── 2. Генерация ответа ───────────────────────────────
        answer, source = await generator.generate(intent)

        llm_ms = int((time.time() - t0) * 1000)

        # ── 3. Логирование ────────────────────────────────────
        log_id = ilogger.log(
            user_id=user_id,
            user_msg=user_text,
            intent=intent,
            bot_answer=answer,
            data_source=source,
            llm_ms=llm_ms,
        )

        ctx.add_message("bot", answer)

        # ── 4. Ответ пользователю ─────────────────────────────
        # VK ограничивает сообщение 4096 символами
        if len(answer) > 4000:
            chunks = [answer[i:i+4000] for i in range(0, len(answer), 4000)]
            for chunk in chunks[:-1]:
                await message.answer(chunk)
            answer = chunks[-1]

        # Формируем финальное сообщение с мета-информацией
        footer = f"\n\n🤖 Ответ сгенерирован ИИ (уверенность: {int(intent.confidence * 100)}%)"

        await message.answer(
            answer + footer,
            keyboard=_suggest_keyboard(intent.category),
        )

        # Предлагаем оценить если есть log_id
        if log_id:
            await message.answer(
                RATING_INTRO,
                keyboard=_rating_keyboard(log_id),
            )
