# Добавляем текущую папку в sys.path для 
# корректного импорта зависимостей в controller

import sys
import os
# Добавляем директорию server в sys.path для корректного абсолютного импорта
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))

from fastapi import APIRouter, Cookie, Depends

from model.schemas.service_appointment_form import ServiceAppointmentForm
from model.services.appointment_service import AppointmentService
from model.services.user_service import UserService
from model.api.dependencies import get_appointment_service, get_user_service

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
    session_token: str | None = Cookie(default=None),
    appointment_service: AppointmentService = Depends(get_appointment_service),
    user_service: UserService = Depends(get_user_service),
    ):
    try:
        current_session = await user_service.validate_session(session_token)
        if current_session['status'] == '200':
            new_appointment = await appointment_service.create_appointment(form, session_token)
            return new_appointment
        return current_session
    except Exception as e:
        return {
            'status': '400',
            'message': f'Ошибка на бекенде: {str(e)}'
        }