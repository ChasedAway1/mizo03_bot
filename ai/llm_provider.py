import os
import logging
import aiohttp
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

# Базовый класс


class BaseLLMProvider(ABC):
    @abstractmethod
    async def complete(self, system: str, user: str) -> str:
        """Отправить запрос, получить строку-ответ."""
        ...


# LLM7.io — ОСНОВНОЙ провайдер

class LLM7Provider(BaseLLMProvider):
    API_URL = "https://api.llm7.io/v1/chat/completions"

    def __init__(self):
        self.model = os.getenv("LLM7_MODEL", "deepseek-v3-0324")

    async def complete(self, system: str, user: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user",   "content": user},
            ],
            "temperature": 0.3,
            "max_tokens":  1024,
        }
        headers = {
            "Authorization": "Bearer unused",
            "Content-Type":  "application/json",
        }
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.API_URL,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30),
                ) as resp:
                    if resp.status == 429:
                        logger.warning("LLM7: превышен лимит 30 RPM")
                        return (
                            "Система временно перегружена. "
                            "Пожалуйста, повторите вопрос через минуту."
                        )
                    data = await resp.json()
                    if "error" in data:
                        logger.error(f"LLM7 error: {data['error']}")
                        return "Произошла ошибка. Попробуйте позже или обратитесь в МИЗО РБ."
                    return data["choices"][0]["message"]["content"]
        except aiohttp.ClientConnectorError:
            logger.error("LLM7: нет соединения")
            return "Сервис временно недоступен. Обратитесь в МИЗО РБ по телефону."
        except Exception as e:
            logger.error(f"LLM7 exception: {e}")
            return "Произошла ошибка при обработке запроса. Попробуйте позже."


# ─────────────────────────────────────────────
# Фабрика
# ─────────────────────────────────────────────

def get_llm_provider() -> BaseLLMProvider:
    backend = os.getenv("LLM_BACKEND", "llm7").lower()
    providers = {
        "llm7":       LLM7Provider,
    }
    cls = providers.get(backend)
    if cls is None:
        raise ValueError(
            f"Неизвестный LLM_BACKEND='{backend}'. "
            f"Допустимые значения: {list(providers)}"
        )
    logger.info(f"LLM провайдер: {backend} | модель: {os.getenv('LLM7_MODEL','deepseek-v3-0324')}")
    return cls()
