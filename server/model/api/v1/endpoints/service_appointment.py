# Добавляем текущую папку в sys.path для 
# корректного импорта зависимостей в controller

import sys
import os
# Добавляем директорию server в sys.path для корректного абсолютного импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from fastapi import APIRouter, Cookie, Response

from model.db.db_service_appointment_dao import ServiceAppointmentDAO
from model.models.models import ServiceAppointmentForm
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

@router.post("/service-appointment")
async def handle_service_appointment(
    form: ServiceAppointmentForm,
    response: Response,
    session_token: str | None = Cookie(default=None)
    ):
    current_session_status = validate_session(response, session_token)
    if current_session_status['status'] != '200':
        return {
            'status': current_session_status['status'],
            'message': current_session_status['message']
        }
    client_id = current_session_status['payload']['user_id']

    async with AsyncSessionMaker() as db_session:
        service_appointment_dao = ServiceAppointmentDAO(db_session)

        existing_appointment = await service_appointment_dao.get_by_date_and_time(form.date, form.time)
        if existing_appointment:
            return {
            'status': '400',
            'message': 'Выбранные время и дата заняты. \
                        Пожалуйста, выберите другие время и дату'
        }

        new_appointment = await service_appointment_dao.create(form.service_name, form.date, form.time, client_id)
        new_appointment_id = new_appointment.id

        return {
                'status': '200',
                'message': f'Запись под номером {new_appointment_id} на услугу {form.service_name} прошла успешно!'
            }