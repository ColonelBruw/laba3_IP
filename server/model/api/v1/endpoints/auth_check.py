import sys
import os
# Добавляем директорию server в sys.path для корректного абсолютного импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from fastapi import APIRouter, Cookie, Response

from model.core.security import validate_session

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
    session_token: str | None = Cookie(default=None)
    ):
    current_session_status = validate_session(response, session_token)
    return current_session_status