# Помещаем в sys.path путь до директории server чтобы работали глобальные импорты
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import re
from typing import List, Optional
from model.db.dao.service_appointment_dao import ServiceAppointmentDAO
from model.core.security import decode_access_token
from model.schemas.service_appointment_form import ServiceAppointmentForm
from model.db.db_base import ServiceAppointment

# Установка локали (при развертывании через контейнер закоментировать)
# import locale
# try:
#     locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
# except:
#     locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

class AppointmentService:
    """Сервис для работы с записями на услуги автосалона"""
    
    def __init__(self, appointment_dao: ServiceAppointmentDAO):
        self.appointment_dao = appointment_dao

    async def get_by_id(self, appointment_id: int) -> Optional[ServiceAppointment]:
        appointment = await self.appointment_dao.get_by_id(appointment_id)
        if not appointment:
            return None
        return appointment
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ServiceAppointment]:
        appointments = await self.appointment_dao.get_all(skip, limit)
        return appointments
    
    async def get_by_time_and_date(self, date_value: str, time_value: str) -> Optional[ServiceAppointment]:
        appointment = await self.appointment_dao.get_by_date_and_time(date_value, time_value)
        if not appointment:
            return None
        return appointment
    
    async def create_appointment(self, appointment_form: ServiceAppointmentForm, session_token: str) -> dict:
        client_id = decode_access_token(session_token).get('user_id')
        existing_appointment = await self.appointment_dao.get_by_date_and_time(appointment_form.date, appointment_form.time)
        if existing_appointment:
            return {
            'status': '400',
            'message': 'Выбранные время и дата заняты. \
                        Пожалуйста, выберите другие время и дату'
        }

        new_appointment = await self.appointment_dao.create_appointment(appointment_form, client_id)
        if new_appointment:
            await self.appointment_dao.session.commit()
            await self.appointment_dao.session.refresh(new_appointment)
            new_appointment_id = new_appointment.id

            return {
                    'status': '200',
                    'message': f'Запись под номером {new_appointment_id} на услугу {appointment_form.service_name} прошла успешно!'
                }
        
    async def update_appointment(self, appointment_id: int, appointment_data: dict) -> Optional[ServiceAppointment]:
        appointment = await self.appointment_dao.update_appointment(appointment_id, **appointment_data)
        if appointment:
            await self.appointment_dao.session.commit()
            return appointment
        return None
    
    async def delete_appointment(self, appointment_id: int) -> bool:
        result = await self.appointment_dao.delete_appointment(appointment_id)
        if result:
            await self.appointment_dao.session.commit()
        return result
    
    async def delete_all_appointments(self) -> int:
        result = await self.appointment_dao.delete_all_appointments()
        if result:
            await self.appointment_dao.session.commit()
        return result  
