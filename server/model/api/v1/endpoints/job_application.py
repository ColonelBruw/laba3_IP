# Добавляем текущую папку в sys.path для 
# корректного импорта зависимостей в другие файлы бекенда

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from fastapi import APIRouter, Cookie, Response

from model.db.db_job_application_dao import JobApplicationDAO
from model.models.models import JobApplicationForm
from model.core.security import validate_session

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
    response: Response,
    session_token: str | None = Cookie(default=None)
    ):
    current_session_status = validate_session(response, session_token)
    if current_session_status['status'] != '200':
        return {
            'status': current_session_status['status'],
            'message': current_session_status['message']
        }
    
    async with AsyncSessionMaker() as db_session:
        job_application_dao = JobApplicationDAO(db_session)

        applicant_id = current_session_status['payload']['user_id']
        new_application = await job_application_dao.create(form.pos, applicant_id)
        new_application_id = new_application.id

    return {
            'status': '200',
            'message': f'Заявка под номером {new_application_id} успешно заполнена!'
        }