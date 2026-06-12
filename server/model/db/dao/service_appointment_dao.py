# Добавляем текущую папку в sys.path 
# для корректного импорта зависимостей в другие файлы бекенда
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, List
from model.db.db_base import ServiceAppointment
from model.schemas.service_appointment_form import ServiceAppointmentForm
import datetime

class ServiceAppointmentDAO:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_appointment(self, appointment_form: ServiceAppointmentForm, client_id: int) -> Optional[ServiceAppointment]:
        try:
            date_value = datetime.datetime.strptime(appointment_form.date, "%Y-%m-%d")
            time_value = datetime.datetime.strptime(appointment_form.time, "%H:%M").time()
            new_appointment = ServiceAppointment(
                service_name=appointment_form.service_name,
                date=date_value,
                time=time_value,
                client_id=client_id
            )
            self.session.add(new_appointment)
            return new_appointment
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def get_by_id(self, appointment_id: int) -> Optional[ServiceAppointment]:
        result = await self.session.execute(
            select(ServiceAppointment).where(ServiceAppointment.id == appointment_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self) -> List[ServiceAppointment]:
        try:
            result = await self.session.execute(select(ServiceAppointment))
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def get_by_date_and_time(self, date_value: str, time_value: str) -> Optional[ServiceAppointment]:
        date_value = datetime.datetime.strptime(date_value, "%Y-%m-%d")
        time_value = datetime.datetime.strptime(time_value, "%H:%M").time()
        try:
            result = await self.session.execute(
                select(ServiceAppointment).where(
                    ServiceAppointment.date == date_value,
                    ServiceAppointment.time == time_value
                )
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def update_appointment(self, appointment_id: int, **kwargs) -> Optional[ServiceAppointment]:
        try:
            result = await self.session.execute(
                select(ServiceAppointment).where(ServiceAppointment.id == appointment_id)
            )
            appointment = result.scalar_one_or_none()
            
            if not appointment:
                return None
            
            for field, value in kwargs.items():
                if hasattr(appointment, field):
                    setattr(appointment, field, value)
            
            await self.session.refresh(appointment)
            return appointment
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def delete_appointment(self, appointment_id: int) -> bool:
        try:
            appointment = await self.get_by_id(appointment_id)
            if not appointment:
                return False
            
            await self.session.delete(appointment)
            return True
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def delete_all_appointments(self) -> int:
        try:
            result = await self.session.execute(select(ServiceAppointment))
            appointments = result.scalars().all()
            count = len(appointments)
            
            for appointment in appointments:
                await self.session.delete(appointment)
            return count
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e