# Добавляем текущую папку в sys.path для 
# корректного импорта зависимостей в другие файлы бекенда
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Необходимые зависимости
import re

# DAO-класс для работы с сессиями авторизации
from ..models.models import RegistrtationRequest
    
# Функция валидации имени пользователя
def registration_data_validation(reg_request: RegistrtationRequest) -> str:
    if not all(bool(re.match('[а-яА-Я]', name)) for name in (reg_request.first_name, reg_request.last_name)):
        return 'Впишите имя и фамилию кириллицей, без цифр и спецсимволов'
    
    if not bool(re.match(r'^(\+7|8)\d{10}$', reg_request.phone)):
        return 'Введите номер телефона в одном из форматов \
                        +7ХХХХХХХХХХ, 8XXXXXXXXXX'
    
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not bool(re.match(email_pattern, reg_request.email)):
        return 'Введите корректную электронную почту'
    
    if reg_request.password != reg_request.confirm_password:
        return 'Введенные пароли не совпадают'
    
    return 'Данные для регистрации успешно заполнены'