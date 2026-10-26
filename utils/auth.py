import bcrypt
from database.db_manager import DatabaseManager


def authenticate_user(username, password):
    """Проверка логина и пароля. Возвращает пользователя или None."""
    db = DatabaseManager()
    
    try:
        user = db.execute_query(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        
        if not user:
            return None
        
        user = user[0]
        
        # Проверка хэша пароля
        if bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            return {
                'id': user['id'],
                'username': user['username'],
                'full_name': user['full_name'],
                'role': user['role']
            }
        
        return None
    finally:
        db.close()