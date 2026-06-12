import sys
import os
# Помещаем в sys.path путь до директории server чтобы работали глобальные импорты
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Необходимые зависимости
import re
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone

# Импорт функции создания sessionmaker'а
from model.db.db_config import get_async_sessionmaker

# Импорт dotenv для доступа к переменным окружения
from dotenv import load_dotenv
import os

load_dotenv()

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM')

AsyncSessionMaker = get_async_sessionmaker()

# Создание контекста для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция для создания хэша пароля
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
 
# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Функция для генерации JWT токена
def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, JWT_ALGORITHM)
    return encode_jwt

# Функция декодирует токен и возвращает payload, если подпись верна
def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token, 
            JWT_SECRET_KEY, 
            algorithms=[JWT_ALGORITHM]
        )
        return payload
    except JWTError:
        return None