# Помещаем в sys.path путь до директории server чтобы работали глобальные импорты
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from fastapi import APIRouter, Depends

from model.schemas.registration_request import RegistrtationRequest
from model.services.user_service import UserService
from model.api.dependencies import get_user_service

# Установка локали (при развертывании через контейнер закоментировать)
# import locale
# try:
#     locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
# except:
#     locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

router = APIRouter()

@router.post('/registration')
async def user_registration(
    reg_request: RegistrtationRequest,
    user_service: UserService = Depends(get_user_service)
):
    try:
        registration_result = await user_service.create_user(reg_request)
        return registration_result
    except Exception as e:
        return {
            'status': '400',
            'message': f'Ошибка на бекенде: {str(e)}'
        }
    