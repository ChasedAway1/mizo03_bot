import json
import logging
import re
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)

@dataclass
class Intent:
    category: str            
    subtopic: str            
    measure_id: Optional[int]  
    confidence: float        
    raw_question: str       


SYSTEM_PROMPT = """Ты — интеллектуальный классификатор запросов для чат-бота МИЗО РБ.
Твоя задача: проанализировать вопрос гражданина и определить его категорию и подтему.

Категории:
- svo          — участники специальной военной операции, военнослужащие, ветераны СВО
- large_family — многодетные семьи (3 и более детей)
- laws         — выписки из законов, нормативные документы, статьи закона
- common       — общие вопросы о работе министерства, контакты, режим работы
- unknown      — вопрос не относится к тематике бота

Подтемы:
- docs       — перечень документов, список бумаг, что нужно принести
- right      — кто имеет право, условия, критерии, требования
- howto      — как получить, порядок действий, куда обращаться, шаги
- law        — выписка из закона, статья, норма, законодательная база
- conditions — условия предоставления, требования, ограничения
- general    — общий вопрос по теме без конкретной подтемы

Меры для СВО:
- 1 — ИЖС (бесплатное предоставление земельного участка для индивидуального жилищного строительства)
- 2 — земля под жилым домом (БЕСПЛАТНОЕ ПРЕДОСТАВЛЕНИЕ ЗЕМЕЛЬНОГО УЧАСТКА ПОД ЖИЛЫМ ДОМОМ)
- 3 — сельскохозяйственное производство (Бесплатное предоставление земельного участка для ведения сельско-хозяйственного производства)

Ответь ТОЛЬКО валидным JSON без пояснений:
{
  "category": "svo|large_family|laws|common|unknown",
  "subtopic": "docs|right|howto|law|conditions|general",
  "measure_id": null,
  "confidence": 0.95
}"""


class IntentClassifier:
    def __init__(self, llm_provider):
        self.llm = llm_provider

    async def classify(self, user_message: str) -> Intent:
        """Классифицировать сообщение пользователя."""
        try:
            response = await self.llm.complete(
                system=SYSTEM_PROMPT,
                user=f"Вопрос гражданина: {user_message}"
            )
            intent_data = self._parse_json(response)
            return Intent(
                category=intent_data.get("category", "unknown"),
                subtopic=intent_data.get("subtopic", "general"),
                measure_id=intent_data.get("measure_id"),
                confidence=float(intent_data.get("confidence", 0.5)),
                raw_question=user_message,
            )
        except Exception as e:
            logger.error(f"Ошибка классификации: {e}")
            return Intent(
                category="unknown",
                subtopic="general",
                measure_id=None,
                confidence=0.0,
                raw_question=user_message,
            )

    def _parse_json(self, text: str) -> dict:
        """Извлечь JSON из ответа LLM (модели иногда добавляют markdown)."""
        text = re.sub(r"```(?:json)?", "", text).strip().rstrip("`").strip()
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if match:
            return json.loads(match.group())
        return {}
