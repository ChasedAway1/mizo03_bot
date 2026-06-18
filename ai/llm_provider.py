"""
llm_provider.py — Универсальный провайдер LLM.

Поддерживаемые бэкенды (задаётся в .env):
  LLM_BACKEND=llm7        — LLM7.io (ОСНОВНОЙ: без регистрации, без ключа, бесплатно)
  LLM_BACKEND=openrouter  — OpenRouter (только email, бесплатные модели)
  LLM_BACKEND=yandexgpt  — YandexGPT API
  LLM_BACKEND=ollama      — локальная модель через Ollama

LLM7.io: никакой регистрации, никакого ключа, работает из России.
Документация: https://llm7.io
"""

import os
import logging
import aiohttp
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# Базовый класс
# ─────────────────────────────────────────────

class BaseLLMProvider(ABC):
    @abstractmethod
    async def complete(self, system: str, user: str) -> str:
        """Отправить запрос, получить строку-ответ."""
        ...


# ─────────────────────────────────────────────
# LLM7.io — ОСНОВНОЙ провайдер
# Без регистрации. Без ключа. Бесплатно.
# Работает из России без VPN.
# ─────────────────────────────────────────────

class LLM7Provider(BaseLLMProvider):
    """
    Сайт: https://llm7.io
    Никакой регистрации и ключей не нужно.
    API_KEY в запросе ставим "unused" — сервис его игнорирует.

    Доступные модели (задаётся в .env через LLM7_MODEL):
      deepseek-r1-0528         — мощная reasoning-модель
      deepseek-v3-0324         — быстрая и умная (РЕКОМЕНДУЕТСЯ)
      gpt-4o-mini-2024-07-18   — хорошо знает русский
      mistral-small-3.1-24b    — экономичная
      gemini-2.5-flash-lite    — быстрая

    Лимит: 30 запросов в минуту (бесплатно, без токена).
    """

    API_URL = "https://api.llm7.io/v1/chat/completions"

    def __init__(self):
        # Модель по умолчанию — deepseek-v3, хорошо понимает русский
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
            "Authorization": "Bearer unused",  # ключ не нужен, но поле обязательно
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
# OpenRouter — резервный провайдер
# Регистрация: openrouter.ai (только email)
# ─────────────────────────────────────────────

class OpenRouterProvider(BaseLLMProvider):
    """
    Документация: https://openrouter.ai/docs
    Переменная:   OPENROUTER_API_KEY
    Модель:       OPENROUTER_MODEL

    Как получить ключ:
      1. openrouter.ai -> Sign In -> Continue with Email
      2. Keys -> Create Key
      3. OPENROUTER_API_KEY=sk-or-v1-...
    """

    API_URL = "https://openrouter.ai/api/v1/chat/completions"

    def __init__(self):
        self.api_key = os.getenv("OPENROUTER_API_KEY", "")
        self.model   = os.getenv("OPENROUTER_MODEL", "google/gemma-3-12b-it:free")

    async def complete(self, system: str, user: str) -> str:
        if not self.api_key:
            return "Ошибка: OPENROUTER_API_KEY не задан."

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
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type":  "application/json",
            "HTTP-Referer":  "https://mizo-rb.ru",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.API_URL, json=payload, headers=headers,
                timeout=aiohttp.ClientTimeout(total=30),
            ) as resp:
                data = await resp.json()
                if "error" in data:
                    logger.error(f"OpenRouter error: {data['error']}")
                    return "Произошла ошибка. Попробуйте позже."
                return data["choices"][0]["message"]["content"]


# ─────────────────────────────────────────────
# YandexGPT — резервный провайдер
# ─────────────────────────────────────────────

class YandexGPTProvider(BaseLLMProvider):
    """
    Переменные: YANDEX_API_KEY, YANDEX_FOLDER_ID
    """
    API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    def __init__(self):
        self.api_key   = os.getenv("YANDEX_API_KEY", "")
        self.folder_id = os.getenv("YANDEX_FOLDER_ID", "")

    async def complete(self, system: str, user: str) -> str:
        payload = {
            "modelUri": f"gpt://{self.folder_id}/yandexgpt-lite",
            "completionOptions": {"stream": False, "temperature": 0.3, "maxTokens": 1024},
            "messages": [
                {"role": "system", "text": system},
                {"role": "user",   "text": user},
            ],
        }
        headers = {
            "Authorization": f"Api-Key {self.api_key}",
            "Content-Type":  "application/json",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(self.API_URL, json=payload, headers=headers) as resp:
                data = await resp.json()
        return data["result"]["alternatives"][0]["message"]["text"]


# ─────────────────────────────────────────────
# Ollama — локальная модель (только для разработки)
# ─────────────────────────────────────────────

class OllamaProvider(BaseLLMProvider):
    """
    Переменные: OLLAMA_URL, OLLAMA_MODEL
    Только для локальной разработки — на Bothost недоступно.
    """
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.model    = os.getenv("OLLAMA_MODEL", "llama3")

    async def complete(self, system: str, user: str) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user",   "content": user},
            ],
            "stream": False,
            "options": {"temperature": 0.3},
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/api/chat", json=payload
            ) as resp:
                data = await resp.json()
        return data["message"]["content"]


# ─────────────────────────────────────────────
# Фабрика
# ─────────────────────────────────────────────

def get_llm_provider() -> BaseLLMProvider:
    backend = os.getenv("LLM_BACKEND", "llm7").lower()
    providers = {
        "llm7":       LLM7Provider,
        "openrouter": OpenRouterProvider,
        "yandexgpt":  YandexGPTProvider,
        "ollama":     OllamaProvider,
    }
    cls = providers.get(backend)
    if cls is None:
        raise ValueError(
            f"Неизвестный LLM_BACKEND='{backend}'. "
            f"Допустимые значения: {list(providers)}"
        )
    logger.info(f"LLM провайдер: {backend} | модель: {os.getenv('LLM7_MODEL','deepseek-v3-0324')}")
    return cls()
