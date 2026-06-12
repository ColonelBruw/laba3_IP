# Помещаем в sys.path путь до директории server чтобы работали глобальные импорты
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from fastapi import APIRouter, Depends, Response

from model.schemas.login_request import LoginRequest
from model.services.user_service import UserService
from model.api.dependencies import get_user_service

# Установка локали (при развертывании через контейнер закоментировать)
# import locale
# try:
#     locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
# except:
#     locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

router = APIRouter()

@router.post('/login')
async def user_login(
    login_request: LoginRequest,
    response: Response,
    user_service: UserService = Depends(get_user_service)
):
    try:
        new_session = await user_service.create_session(login_request)
        if new_session['status'] == '200':
            response.set_cookie(
                key="session_token",
                value=new_session['token'],
                httponly=True,  
                max_age=900,   # 15 минут
                secure=False,  
                samesite="lax", # Защищает от CSRF
                path="/"
            )
            
        return {
            'status': new_session['status']
        }
    except Exception as e:
        return {
            'status': '400',
            'message': f'Ошибка на бекенде: {str(e)}'
        }