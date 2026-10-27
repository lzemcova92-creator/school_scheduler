import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Загружаем переменные из файла .env
load_dotenv()

class DatabaseManager:
    def __init__(self):
        # Берем строку подключения из .env
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            raise ValueError("Не найдена переменная DATABASE_URL в файле .env")
        
        # Подключаемся к облачной БД
        self.conn = psycopg2.connect(db_url)
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

    def execute_query(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            self.conn.commit()
            
            # Если это SELECT, возвращаем данные
            if self.cursor.description:
                return self.cursor.fetchall()
            return []
        except Exception as e:
            self.conn.rollback()
            print(f"Ошибка БД: {e}")
            raise

    def close(self):
        self.cursor.close()
        self.conn.close()