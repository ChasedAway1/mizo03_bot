import psycopg2
import psycopg2.extras

class Database:
    def __init__(self, host="aws-1-eu-central-1.pooler.supabase.com", port=5432, database="postgres", user="postgres.gfczyycvyyqmdcqyfmxq", password="Chased_Away1"):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.conn = None
    
    def connect(self):
        """Синхронное подключение к PostgreSQL"""
        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password
        )
        return self.conn
    
    def close(self):
        if self.conn:
            self.conn.close()
    
    def get_cursor(self):
        if not self.conn:
            self.connect()
        return self.conn.cursor()
    
    # Методы для СВО
    def get_svo_title(self, measure_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT title FROM svo_measures WHERE measure_id = %s", (measure_id,))
        result = cursor.fetchone()
        return result[0] if result else "Информация временно недоступна"
    
    def get_svo_docs(self, measure_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT docs FROM svo_measures WHERE measure_id = %s", (measure_id,))
        result = cursor.fetchone()
        return result[0] if result else "Информация временно недоступна"
    
    def get_svo_right(self, measure_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT right_text FROM svo_measures WHERE measure_id = %s", (measure_id,))
        result = cursor.fetchone()
        return result[0] if result else "Информация временно недоступна"
    
    def get_svo_conditions(self, measure_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT conditions FROM svo_measures WHERE measure_id = %s", (measure_id,))
        result = cursor.fetchone()
        return result[0] if result else "Информация временно недоступна"
    
    def get_svo_howto(self, measure_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT howto FROM svo_measures WHERE measure_id = %s", (measure_id,))
        result = cursor.fetchone()
        return result[0] if result else "Информация временно недоступна"
    
    def get_svo_law(self, measure_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT law FROM svo_measures WHERE measure_id = %s", (measure_id,))
        result = cursor.fetchone()
        return result[0] if result else "Информация временно недоступна"
    
    # Методы для многодетных
    def get_large_law(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT law FROM large_family WHERE id = 1")
        result = cursor.fetchone()
        return result[0] if result else "Информация временно недоступна"
    
    def get_large_conditions(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT conditions FROM large_family WHERE id = 1")
        result = cursor.fetchone()
        return result[0] if result else "Информация временно недоступна"
    
    def get_large_order(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT order_text FROM large_family WHERE id = 1")
        result = cursor.fetchone()
        return result[0] if result else "Информация временно недоступна"
    
    # Методы для закона
    def get_laws_part(self, part_id):
        cursor = self.get_cursor()
        cursor.execute("SELECT part_text FROM laws_parts WHERE part_id = %s", (part_id,))
        result = cursor.fetchone()
        return result[0] if result else "Информация временно недоступна"
    
    # Метод для общих вопросов
    def get_common_text(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT text FROM common WHERE id = 1")
        result = cursor.fetchone()
        return result[0] if result else "Информация будет добавлена позже."