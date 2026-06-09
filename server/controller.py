# Добавляем текущую папку в sys.path для 
# корректного импорта зависимостей в другие файлы бекенда

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Импорт FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Импорт роутера со всеми эндпоинтами
from model.api.v1.routers import router

# Установка локали (при развертывании через контейнер закоментировать)
# import locale
# try:
#     locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
# except:
#     locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

app = FastAPI()

# Настройка CORS для разрешения запросов с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

app.include_router(router, prefix="/api/v1/endpoints")

@app.get("/")
async def root():
    return {"message": "FastAPI for CarFast is running"}
