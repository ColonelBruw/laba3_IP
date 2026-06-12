# Добавляем текущую папку в sys.path для 
# корректного импорта зависимостей в другие файлы бекенда

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from fastapi import APIRouter, Cookie, Depends

from model.schemas.job_application_form import JobApplicationForm
from model.api.dependencies import get_job_application_service, get_user_service, JobApplicationService, UserService

from model.db.db_config import get_async_sessionmaker

# Установка локали (при развертывании через контейнер закоментировать)
# import locale
# try:
#     locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
# except:
#     locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

router = APIRouter()

AsyncSessionMaker = get_async_sessionmaker()

@router.post("/job-application")
async def handle_job_application(
    form: JobApplicationForm,
    job_application_service: JobApplicationService = Depends(get_job_application_service),
    user_service: UserService = Depends(get_user_service),
    session_token: str | None = Cookie(default=None)
    ):
    try:
        session_status = await user_service.validate_session(session_token)
        if session_status['status'] == '200':
            new_application = await job_application_service.create_application(form, session_token)
            return new_application
        return session_status
    except Exception as e:
        return {
            'status': '400',
            'message': f'Ошибка на бекенде: {str(e)}'
        }