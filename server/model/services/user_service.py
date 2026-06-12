# Помещаем в sys.path путь до директории server чтобы работали глобальные импорты
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import re
from typing import List, Optional
from jose import ExpiredSignatureError
from model.db.dao.user_dao import UserDAO
from model.core.security import get_password_hash, create_access_token, decode_access_token, verify_password
from model.schemas.registration_request import RegistrtationRequest
from model.schemas.login_request import LoginRequest
from model.db.db_base import User

# Установка локали (при развертывании через контейнер закоментировать)
# import locale
# try:
#     locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
# except:
#     locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

class UserService:
    """Сервис для работы с пользователями"""
    
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        user = await self.user_dao.get_by_id(user_id)
        if not user:
            return None
        return user
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        users = await self.user_dao.get_all(skip, limit)
        return users
    
    async def get_by_email(self, email: str) -> Optional[User]:
        user = await self.user_dao.get_by_email(email)
        if not user:
            return None
        return user
    
    async def get_by_phone(self, phone: str) -> Optional[User]:
        user = await self.user_dao.get_by_phone(phone)
        if not user:
            return None
        return user
    
    async def get_by_name(self, first_name: str, last_name: str) -> Optional[User]:
        user = await self.user_dao.get_by_name(first_name, last_name)
        if not user:
            return None
        return user
    
    async def create_user(self, user_data: RegistrtationRequest) -> dict:
        validation_status = self.registration_data_validation(user_data)

        if validation_status != 'Данные для регистрации успешно заполнены':
            return {
                'status': '400',
                'message': validation_status
                }
        
        hashed_password = get_password_hash(user_data.password)
        new_user = await self.user_dao.create_user(
            first_name=user_data.first_name.lower().capitalize(),
            last_name=user_data.last_name.lower().capitalize(),
            phone_number=user_data.phone if user_data.phone[0] == '8' else user_data.phone[1:],
            email=user_data.email,
            password=hashed_password)
        if new_user:
            await self.user_dao.session.commit()
            await self.user_dao.session.refresh(new_user)
            return {
                    'status': '200',
                    'message': f'Пользователь {new_user.first_name} {new_user.last_name} успешно зарегистрирован под номером {new_user.id}'
                    }
        else:
            return {
                'status': '400',
                'message': 'Ошибка при регистрации'
                }
    
    async def update_user(self, user_id: int, user_data: dict) -> Optional[User]:
        user = await self.user_dao.update_user(user_id, **user_data)
        if user:
            await self.user_dao.session.commit()
            return user
        return None
    
    async def delete_user(self, user_id: int) -> bool:
        result = await self.user_dao.delete_user(user_id)
        if result:
            await self.user_dao.session.commit()
        return result
    
    async def delete_all_users(self) -> int:
        result = await self.user_dao.delete_all_users()
        if result:
            await self.user_dao.session.commit()
        return result
    
    async def create_session(self, login_request: LoginRequest) -> dict:
        user_first_name = login_request.first_name.lower().capitalize()
        user_last_name = login_request.last_name.lower().capitalize()

        user_to_login = await self.user_dao.get_by_name(user_first_name, user_last_name)

        if not user_to_login:
                return {
                    'status': '401',
                    'message': "Пользователя с таким именем и/или паролем не существует"
                }
        hashed_password = user_to_login[0].password
        if not verify_password(login_request.password, hashed_password):
            return {
                'status': '401',
                'message': "Пользователя с таким именем и/или паролем не существует"
                }

        session_token= create_access_token({'user_id': user_to_login[0].id, 'first_name': user_to_login[0].first_name, 'last_name': user_to_login[0].last_name})
        
        return {
            'status': '200',
            'token': session_token
        }
    
    async def validate_session(self, session_token: str | None) -> dict:
        if session_token:
            try:
                payload = decode_access_token(session_token)
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
        
    # Функция валидации имени пользователя
    def registration_data_validation(self, user_data: RegistrtationRequest) -> str:
        if not all(bool(re.match('[а-яА-Я]', name)) for name in (user_data.first_name, user_data.last_name)):
            return 'Впишите имя и фамилию кириллицей, без цифр и спецсимволов'
        
        if not bool(re.match(r'^(\+7|8)\d{10}$', user_data.phone)):
            return 'Введите номер телефона в одном из форматов \
                            +7ХХХХХХХХХХ, 8XXXXXXXXXX'
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not bool(re.match(email_pattern, user_data.email)):
            return 'Введите корректную электронную почту'
        
        if user_data.password != user_data.confirm_password:
            return 'Введенные пароли не совпадают'
        
        return 'Данные для регистрации успешно заполнены'
