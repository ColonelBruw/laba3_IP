# Помещаем в sys.path путь до директории server чтобы работали глобальные импорты
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from fastapi import APIRouter

from model.db.db_user_dao import UserDAO
from model.core.security import get_password_hash
from model.models.models import RegistrtationRequest
from model.api.dependencies import registration_data_validation

# Импорт функции создания sessionmaker'а
from model.db.db_config import get_async_sessionmaker

# Установка локали (при развертывании через контейнер закоментировать)
# import locale
# try:
#     locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
# except:
#     locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

router = APIRouter()

AsyncSessionMaker = get_async_sessionmaker()

@router.post('/registration')
async def user_registration(
    reg_request: RegistrtationRequest
):
    async with AsyncSessionMaker() as session:
        user_dao = UserDAO(session)

        validation_status = registration_data_validation(reg_request)

        if validation_status != 'Данные для регистрации успешно заполнены':
            return {
            'status': '400',
            'message': validation_status
            }
        
        hashed_password = get_password_hash(reg_request.password)
        new_user = await user_dao.create(
            first_name=reg_request.first_name.lower().capitalize(),
            last_name=reg_request.last_name.lower().capitalize(),
            phone_number=reg_request.phone if reg_request.phone[0] == '8' else reg_request.phone[1:],
            email=reg_request.email,
            password=hashed_password)
        new_user_id = new_user.id

        return {
            'status': '200',
            'message': f'Пользователь {reg_request.first_name} {reg_request.last_name} успешно зарегистрирован под номером {new_user_id}'
        }