<<<<<<< HEAD
=======
"""
context_manager.py — Управление диалоговым контекстом.

Хранит историю последних N сообщений каждого пользователя в памяти
(без персистентности — достаточно для демонстрации на защите).
"""

>>>>>>> 4b55dc7883198cb626e17712fddf1c30aa32cf26
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Deque


@dataclass
class Message:
<<<<<<< HEAD
    role: str      
=======
    role: str       # "user" | "bot"
>>>>>>> 4b55dc7883198cb626e17712fddf1c30aa32cf26
    text: str
    timestamp: float = field(default_factory=time.time)


class UserContext:
    """Контекст одного пользователя."""

    MAX_HISTORY = 10          # максимум сообщений в памяти
    SESSION_TTL = 30 * 60     # 30 минут — сессия сбрасывается

    def __init__(self, user_id: int):
        self.user_id: int = user_id
        self.history: Deque[Message] = deque(maxlen=self.MAX_HISTORY)
<<<<<<< HEAD
        self.last_category: str | None = None   
        self.last_measure: int | None = None    
=======
        self.last_category: str | None = None   # последняя категория (svo/large...)
        self.last_measure: int | None = None    # последняя мера СВО
>>>>>>> 4b55dc7883198cb626e17712fddf1c30aa32cf26
        self._last_active: float = time.time()

    def add_message(self, role: str, text: str) -> None:
        self.history.append(Message(role=role, text=text))
        self._last_active = time.time()

    def update_from_intent(self, intent) -> None:
        """Обновить контекст по результату классификации."""
        if intent.category != "unknown":
            self.last_category = intent.category
        if intent.measure_id is not None:
            self.last_measure = intent.measure_id

    def is_expired(self) -> bool:
        return (time.time() - self._last_active) > self.SESSION_TTL

    def get_history_text(self) -> str:
        """Последние N сообщений в виде текста для LLM."""
        lines = []
        for msg in self.history:
            prefix = "Пользователь" if msg.role == "user" else "Бот"
            lines.append(f"{prefix}: {msg.text}")
        return "\n".join(lines)

    def reset(self) -> None:
        self.history.clear()
        self.last_category = None
        self.last_measure  = None


class ContextManager:
    """Глобальный менеджер контекстов всех пользователей."""

    def __init__(self):
        self._contexts: dict[int, UserContext] = {}

    def get(self, user_id: int) -> UserContext:
        ctx = self._contexts.get(user_id)
        if ctx is None or ctx.is_expired():
            ctx = UserContext(user_id)
            self._contexts[user_id] = ctx
        return ctx

    def cleanup_expired(self) -> int:
<<<<<<< HEAD
        """Удалить старые контексты. Возвращает количество удалённых."""
=======
        """Удалить протухшие контексты. Возвращает количество удалённых."""
>>>>>>> 4b55dc7883198cb626e17712fddf1c30aa32cf26
        expired = [uid for uid, ctx in self._contexts.items() if ctx.is_expired()]
        for uid in expired:
            del self._contexts[uid]
        return len(expired)
