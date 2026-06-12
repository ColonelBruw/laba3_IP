# Добавляем текущую папку в sys.path для 
# корректного импорта зависимостей в другие файлы бекенда
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Необходимые зависимости
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from model.db.dao.user_dao import UserDAO
from model.db.dao.service_appointment_dao import ServiceAppointmentDAO
from model.db.dao.job_application_dao import JobApplicationDAO
from model.db.db_config import get_async_sessionmaker

from model.services.user_service import UserService
from model.services.appointment_service import AppointmentService
from model.services.job_application_service import JobApplicationService

async def get_user_dao(
    session: AsyncSession = Depends(get_async_sessionmaker)
) -> UserDAO:
    """Dependency для получения UserDAO для взаимодействия с пользователями"""
    return UserDAO(session)

async def get_service_appointment_dao(
    session: AsyncSession = Depends(get_async_sessionmaker)
) -> ServiceAppointmentDAO:
    """Dependency для получения ServiceAppointmentDAO для взаимодействия с записями на услуги"""
    return ServiceAppointmentDAO(session)

async def get_job_application_dao(
    session: AsyncSession = Depends(get_async_sessionmaker)
) -> JobApplicationDAO:
    """Dependency для получения JobApplicationDAO для взаимодействия с заявками на работу"""
    return JobApplicationDAO(session)



async def get_user_service(
    user_dao: UserDAO = Depends(get_user_dao)
) -> UserService:
    """Dependency для получения сервиса User"""
    return UserService(user_dao)

async def get_appointment_service(
    appointment_dao: AsyncSession = Depends(get_service_appointment_dao)
) -> AppointmentService:
    """Dependency для получения сервиса ServiceAppointment"""
    return AppointmentService(appointment_dao)

async def get_job_application_service(
    job_application_dao: AsyncSession = Depends(get_job_application_dao)
) -> JobApplicationService:
    """Dependency для получения сервиса JobApplication"""
    return JobApplicationService(job_application_dao)
