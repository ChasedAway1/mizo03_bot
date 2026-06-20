import logging
from typing import Optional
from .intent_classifier import Intent

logger = logging.getLogger(__name__)

ANSWER_SYSTEM_PROMPT = """Ты — вежливый и компетентный помощник Министерства имущественных
и земельных отношений Республики Бурятия (МИЗО РБ).

Твоя задача: на основе предоставленных данных из базы законодательства дать
чёткий, понятный ответ гражданину. 

Правила:
1. Отвечай ТОЛЬКО на основе предоставленного контекста — не придумывай данные.
2. Если в контексте есть ссылки на закон — обязательно упоминай их.
3. Структурируй ответ: используй нумерацию или перечисление где уместно.
4. Говори официально, но понятно простому гражданину.
5. В конце добавь: "По дополнительным вопросам обращайтесь в МИЗО РБ."
6. Если данных недостаточно — честно сообщи об этом и укажи, куда обратиться.
7. Ответ на русском языке. Максимум 4000 символов.
8. НЕ используй markdown-форматирование: никаких **, *, #, __, []() и других символов разметки. Только plain text.
9. НЕ ПРИДУМЫВАЙ ЗАКОНЫ ЕСЛИ ХОЧЕШЬ УПОМЯНУТЬ КАКОЙ ТО ЗАКОН УКАЖИ Закон Республики Бурятия от 16.10.2002 № 115-III
10. Если тебе задают вопрос связанный с информацией из базы данных (например, какие меры поддержки есть для участников СВО?) тебе надо назвать все меры поддержки из этого контекста какие документы нужны кто может получить кто имеет право получить и как получить участок. Ответы у тебя есть в базе данных мер СВО или многодетных
"""

class AnswerGenerator:
    def __init__(self, llm_provider, db):
        self.llm = llm_provider
        self.db  = db

    async def generate(self, intent: Intent) -> tuple[str, str]:
        # Возвращает (ответ_LLM, источник_данных). источник_данных - строка для логирования/отладки.
        context, source = self._retrieve_context(intent)

        if not context:
            return (
                "К сожалению, по вашему вопросу информация не найдена. "
                "Пожалуйста, обратитесь в МИЗО РБ напрямую.",
                "no_data"
            )

        user_prompt = (
            f"Вопрос гражданина: {intent.raw_question}\n\n"
            f"Данные из законодательной базы МИЗО РБ:\n{context}"
        )

        try:
            answer = await self.llm.complete(
                system=ANSWER_SYSTEM_PROMPT,
                user=user_prompt
            )
            return answer, source
        except Exception as e:
            logger.error(f"Ошибка генерации ответа: {e}")
            return (
                "Произошла ошибка при обработке запроса. "
                "Пожалуйста, попробуйте позже или обратитесь в МИЗО РБ.",
                "llm_error"
            )

    def _retrieve_context(self, intent: Intent) -> tuple[str, str]:
        # Извлечь релевантные данные из БД по намерению.
        cat = intent.category
        sub = intent.subtopic
        mid = intent.measure_id

        if cat == "svo":
            if mid:
                return self._get_svo_context(mid, sub)
            else:
                # Нет конкретной меры — возвращаем сводку всех трёх
                parts = []
                for m in (1, 2, 3):
                    title = self.db.get_svo_title(m)
                    parts.append(f"Мера {m}: {title}")
                return "\n".join(parts), f"svo_all"

        if cat == "large_family":
            return self._get_large_context(sub)

        if cat == "laws":
            parts = []
            for i in range(1, 7):
                part = self.db.get_laws_part(i)
                if part and part != "Информация временно недоступна":
                    parts.append(f"Часть {i}:\n{part}")
            return "\n\n".join(parts), "laws_all"

        if cat == "common":
            text = self.db.get_common_text()
            return text, "common"

        return "", "unknown"

    def _get_svo_context(self, measure_id: int, subtopic: str) -> tuple[str, str]:
        # Получить контекст для конкретной меры СВО.
        title      = self.db.get_svo_title(measure_id)
        docs       = self.db.get_svo_docs(measure_id)
        right_text = self.db.get_svo_right(measure_id)
        conditions = self.db.get_svo_conditions(measure_id)
        howto      = self.db.get_svo_howto(measure_id)
        law        = self.db.get_svo_law(measure_id)

        # Если подтема конкретная — включаем её первой + закон для ссылки
        if subtopic == "docs":
            ctx = f"Мера: {title}\n\nПеречень документов:\n{docs}\n\nПравовая основа:\n{law}"
        elif subtopic in ("right", "conditions"):
            ctx = (
                f"Мера: {title}\n\n"
                f"Кто имеет право:\n{right_text}\n\n"
                f"Условия получения:\n{conditions}\n\n"
                f"Правовая основа:\n{law}"
            )
        elif subtopic == "howto":
            ctx = (
                f"Мера: {title}\n\n"
                f"Как получить (порядок действий):\n{howto}\n\n"
                f"Необходимые документы:\n{docs}\n\n"
                f"Правовая основа:\n{law}"
            )
        elif subtopic == "law":
            ctx = f"Мера: {title}\n\nВыписка из закона:\n{law}"
        else:
            # general — полный контекст
            ctx = (
                f"Мера: {title}\n\n"
                f"Кто имеет право:\n{right_text}\n\n"
                f"Условия:\n{conditions}\n\n"
                f"Документы:\n{docs}\n\n"
                f"Как получить:\n{howto}\n\n"
                f"Правовая основа:\n{law}"
            )
        return ctx, f"svo_measure_{measure_id}_{subtopic}"

    def _get_large_context(self, subtopic: str) -> tuple[str, str]:
        # Получить контекст для многодетных семей.
        law        = self.db.get_large_law()
        conditions = self.db.get_large_conditions()
        order      = self.db.get_large_order()

        if subtopic == "law":
            ctx = f"Выписка из закона (многодетные семьи):\n{law}"
        elif subtopic in ("right", "conditions"):
            ctx = f"Условия предоставления земли многодетным семьям:\n{conditions}\n\nПравовая основа:\n{law}"
        elif subtopic == "howto":
            ctx = (
                f"Порядок предоставления земли многодетным семьям:\n{order}\n\n"
                f"Условия:\n{conditions}\n\n"
                f"Правовая основа:\n{law}"
            )
        else:
            ctx = (
                f"Выписка из закона:\n{law}\n\n"
                f"Условия предоставления:\n{conditions}\n\n"
                f"Порядок предоставления:\n{order}"
            )
        return ctx, f"large_family_{subtopic}"
