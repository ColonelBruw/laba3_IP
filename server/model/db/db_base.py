# Добавляем текущую папку в sys.path для 
# корректного импорта зависимостей в другие файлы бекенда

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from typing import TypeVar
import asyncio
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Time, text
from sqlalchemy.ext.asyncio import create_async_engine

# Установка локали (при развертывании через контейнер закоментировать)
# import locale
# try:
#     locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
# except:
#     locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

from dotenv import load_dotenv
import os

load_dotenv()

# Тип-переменная для модели SQLAlchemy
ModelType = TypeVar('ModelType', bound=DeclarativeBase)

class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy"""
    pass

# Таблица с пользователями
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(30), nullable=False)
    last_name = Column(String(30), nullable=False)
    phone_number = Column(String(11), nullable=True)
    email = Column(String(30), nullable=True)
    password = Column(String(60), nullable=True)

    is_user: Mapped[bool] = mapped_column(default=True, server_default=text('true'), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, server_default=text('false'), nullable=False)

    job_application = relationship("JobApplication", back_populates="applicant")
    service_appointment = relationship("ServiceAppointment", back_populates="client")

    extend_existing = True

# Таблица с заявками на работу
class JobApplication(Base):
    __tablename__ = 'job_applications'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    position_name = Column(String(30), nullable=False)
    applicant_id = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    
    applicant = relationship("User", back_populates="job_application")

# Таблица с записями в автосалон
class ServiceAppointment(Base):
    __tablename__ = 'service_appointments'

    id = Column(Integer, primary_key=True)
    service_name = Column(String(30), nullable=False)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    client_id = Column(Integer, ForeignKey('users.id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    
    client = relationship("User", back_populates="service_appointment")

DB_DRIVER = os.getenv('DB_DRIVER')
DB_DIALECT = os.getenv('DB_DIALECT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

DATABASE_URL = f"{DB_DRIVER}+{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(DATABASE_URL, echo=False, pool_size=5, max_overflow=10)

# Функция удаления таблиц
async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

# Функция создания таблиц
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    await drop_tables()
    await create_tables()

if __name__ == "__main__":
    asyncio.run(main())
