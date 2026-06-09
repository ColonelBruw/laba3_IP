# Добавляем текущую папку в sys.path 
# для корректного импорта зависимостей в другие файлы бекенда
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from typing import Optional, List
from db_base import ServiceAppointment
import datetime

class ServiceAppointmentDAO:

    def __init__(self, session):
        self.session = session

    async def create(self, service_name: str, date_value: str, time_value: str, client_id: int) -> Optional[ServiceAppointment]:
        try:
            date_value = datetime.datetime.strptime(date_value, "%Y-%m-%d")
            time_value = datetime.datetime.strptime(time_value, "%H:%M").time()
            new_appointment = ServiceAppointment(
                service_name=service_name,
                date=date_value,
                time=time_value,
                client_id=client_id
            )
            self.session.add(new_appointment)
            await self.session.commit()
            await self.session.refresh(new_appointment)
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
    
    async def update(self, appointment_id: int, **kwargs) -> Optional[ServiceAppointment]:
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
            
            await self.session.commit()
            await self.session.refresh(appointment)
            return appointment
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def delete(self, appointment_id: int) -> bool:
        try:
            appointment = await self.get_by_id(appointment_id)
            if not appointment:
                return False
            
            await self.session.delete(appointment)
            await self.session.commit()
            return True
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def delete_all(self) -> int:
        try:
            result = await self.session.execute(select(ServiceAppointment))
            appointments = result.scalars().all()
            count = len(appointments)
            
            for appointment in appointments:
                await self.session.delete(appointment)
            
            await self.session.commit()
            return count
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e