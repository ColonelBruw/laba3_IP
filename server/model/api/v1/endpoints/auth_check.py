import sys
import os
# Добавляем директорию server в sys.path для корректного абсолютного импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from fastapi import APIRouter, Depends, Response, Cookie

from model.services.user_service import UserService
from model.api.dependencies import get_user_service

# Установка локали (при развертывании через контейнер закоментировать)
# import locale
# try:
#     locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
# except:
#     locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

router = APIRouter()

@router.post("/auth-check")
async def authorization_check(
    response: Response,
    session_token: str | None = Cookie(default=None),
    user_service: UserService = Depends(get_user_service)
    ):
    try:
        current_session_status = await user_service.validate_session(session_token)
        if current_session_status['status'] == '401':
            response.delete_cookie(key='session_key')
        return current_session_status
    except Exception as e:
        return {
            'status': '400',
            'message': f'Ошибка на бекенде: {str(e)}'
        }