<<<<<<< HEAD
=======
"""
interaction_logger.py — Логирование взаимодействий пользователь ↔ бот.

Сохраняет в таблицу interaction_logs:
  - вопрос пользователя
  - определённое намерение (категория, подтема, мера)
  - сгенерированный ответ
  - источник данных
  - время ответа LLM
  - оценку пользователя (если поставил)
"""

>>>>>>> 4b55dc7883198cb626e17712fddf1c30aa32cf26
import time
import logging
from typing import Optional

logger = logging.getLogger(__name__)

<<<<<<< HEAD
=======

>>>>>>> 4b55dc7883198cb626e17712fddf1c30aa32cf26
class InteractionLogger:
    def __init__(self, db):
        self.db = db
        self._ensure_table()

    def _ensure_table(self):
        """Создать таблицу логов если не существует."""
        try:
            cursor = self.db.get_cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS interaction_logs (
                    id          SERIAL PRIMARY KEY,
                    user_id     BIGINT       NOT NULL,
                    user_msg    TEXT         NOT NULL,
                    category    VARCHAR(50),
                    subtopic    VARCHAR(50),
                    measure_id  INTEGER,
                    confidence  FLOAT,
                    bot_answer  TEXT,
                    data_source VARCHAR(100),
                    llm_ms      INTEGER,
                    rating      INTEGER,
                    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.db.conn.commit()
        except Exception as e:
            logger.error(f"Не удалось создать таблицу interaction_logs: {e}")

    def log(
        self,
        user_id: int,
        user_msg: str,
        intent,
        bot_answer: str,
        data_source: str,
        llm_ms: int,
    ) -> Optional[int]:
        """Записать взаимодействие. Возвращает id записи."""
        try:
            cursor = self.db.get_cursor()
            cursor.execute("""
                INSERT INTO interaction_logs
                  (user_id, user_msg, category, subtopic, measure_id,
                   confidence, bot_answer, data_source, llm_ms)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                user_id,
                user_msg,
                intent.category,
                intent.subtopic,
                intent.measure_id,
                intent.confidence,
                bot_answer,
                data_source,
                llm_ms,
            ))
            log_id = cursor.fetchone()[0]
            self.db.conn.commit()
            return log_id
        except Exception as e:
            logger.error(f"Ошибка логирования: {e}")
            return None

    def save_rating(self, log_id: int, rating: int) -> bool:
        """Сохранить оценку пользователя (1–5)."""
        try:
            cursor = self.db.get_cursor()
            cursor.execute(
                "UPDATE interaction_logs SET rating = %s WHERE id = %s",
                (rating, log_id)
            )
            self.db.conn.commit()
            return True
        except Exception as e:
            logger.error(f"Ошибка сохранения оценки: {e}")
            return False

    def get_stats(self) -> dict:
        """Статистика для администратора."""
        try:
            cursor = self.db.get_cursor()
            cursor.execute("""
                SELECT
                    COUNT(*)                              AS total,
                    AVG(llm_ms)                           AS avg_ms,
                    AVG(confidence)                       AS avg_conf,
                    AVG(rating)                           AS avg_rating,
                    COUNT(CASE WHEN category='svo'          THEN 1 END) AS svo_cnt,
                    COUNT(CASE WHEN category='large_family' THEN 1 END) AS large_cnt,
                    COUNT(CASE WHEN category='laws'         THEN 1 END) AS laws_cnt,
                    COUNT(CASE WHEN category='unknown'      THEN 1 END) AS unknown_cnt
                FROM interaction_logs
            """)
            row = cursor.fetchone()
            return {
                "total":         row[0],
                "avg_ms":        round(row[1] or 0),
                "avg_confidence":round(float(row[2] or 0), 2),
                "avg_rating":    round(float(row[3] or 0), 2),
                "svo":           row[4],
                "large_family":  row[5],
                "laws":          row[6],
                "unknown":       row[7],
            }
        except Exception as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return {}
