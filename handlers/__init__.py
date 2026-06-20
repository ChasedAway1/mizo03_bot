from .main_handlers import register_main_handlers
from .ai_handler import register_ai_handler

# Старые статические обработчики — оставляем для кнопок
from .svo_handlers import register_svo_handlers
from .large_handlers import register_large_handlers
from .laws_handlers import register_laws_handlers
from .common_handlers import register_common_handlers

__all__ = [
    "register_main_handlers",
    "register_ai_handler",
    "register_svo_handlers",
    "register_large_handlers",
    "register_laws_handlers",
    "register_common_handlers",
]
