# Добавляем текущую папку в sys.path для 
# корректного импорта зависимостей в другие файлы бекенда

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

# Импорт dotenv для доступа к переменным окружения
from dotenv import load_dotenv

load_dotenv()

DB_DRIVER = os.getenv('DB_DRIVER')
DB_DIALECT = os.getenv('DB_DIALECT')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')

# Создание сессии
def get_async_sessionmaker():
    # Создание engine и сессии
    DATABASE_URL = f"{DB_DRIVER}+{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_async_engine(DATABASE_URL, echo=False, pool_size=5, max_overflow=10)

    # Фабрика сессий
    try:
        AsyncSessionMaker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
        return AsyncSessionMaker
    except Exception as e:
        print(f'Не удалось создать sessionmaker: {e}')
        return None