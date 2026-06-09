import sys
import os
# Помещаем в sys.path путь до директории server чтобы работали глобальные импорты
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Необходимые зависимости
from passlib.context import CryptContext
from jose import JWTError, jwt, ExpiredSignatureError
from datetime import datetime, timedelta, timezone
from fastapi import Response

# DAO-класс для работы с пользователями
from model.db.db_user_dao import UserDAO

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
    
# Функция создания сессии
async def create_session(first_name: str, last_name: str, response: Response) -> str:
    async with AsyncSessionMaker() as db_session:
        user_dao = UserDAO(db_session)

        user_to_login = await user_dao.get_by_name(first_name, last_name)
        session_token= create_access_token({'user_id': user_to_login[0].id, 'first_name': user_to_login[0].first_name, 'last_name': user_to_login[0].last_name})
        
        # Создаем куку сессии
        response.set_cookie(
            key="session_token",
            value=session_token,
            httponly=True,  
            max_age=900,   # 15 минут
            secure=False,  
            samesite="lax", # Защищает от CSRF
            path="/"
        )
        
        return session_token

# # Функция провекри валидности сессии
def validate_session(response: Response, session_token: str | None) -> dict:
    if session_token:
        try:
            payload = jwt.decode(session_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            exp_time = payload.get('exp')
            if datetime.now(timezone.utc) >= datetime.fromtimestamp(exp_time, tz=timezone.utc):
                response.delete_cookie(key='session_key')
                return {
                    'status': '401',
                    'message': "Сессия истекла. Авторизуйтесь повторно"
                }
            return {
                'status': '200',
                'message': 'Сессия действительна',
                'payload': payload
            }
        except ExpiredSignatureError:
            return {
            'status': '401',
            'message': 'Ваша сессия истекла. Пожалуйста, авторизуйтесь повторно'
        }
    else:
        return {
            'status': '401',
            'message': 'Для продолжения необходимо авторизоваться'
        }