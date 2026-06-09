# Помещаем в sys.path путь до директории server чтобы работали глобальные импорты
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from fastapi import APIRouter, Response

from model.db.db_user_dao import UserDAO
from model.models.models import LoginRequest
from model.core.security import verify_password, create_session

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

@router.post('/login')
async def user_login(
    login_request: LoginRequest,
    response: Response
):
    async with AsyncSessionMaker() as session:
        user_dao = UserDAO(session)

        first_name = login_request.first_name.lower().capitalize()
        last_name = login_request.last_name.lower().capitalize()
        user_to_login = await user_dao.get_by_name(first_name, last_name)
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

        new_session_token = await create_session(first_name, last_name, response)

        return {
            'status': '200'
        }