# Добавляем текущую папку в sys.path для 
# корректного импорта зависимостей в другие файлы бекенда

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import APIRouter

from endpoints import registration, login, job_application, service_appointment, auth_check, logout

# Установка локали (при развертывании через контейнер закоментировать)
# import locale
# try:
#     locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
# except:
#     locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

router = APIRouter()

router.include_router(registration.router)
router.include_router(login.router)
router.include_router(job_application.router)
router.include_router(service_appointment.router)
router.include_router(auth_check.router)
router.include_router(logout.router)