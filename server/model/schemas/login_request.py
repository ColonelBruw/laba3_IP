# Добавляем текущую папку в sys.path для 
# корректного импорта зависимостей в другие файлы бекенда
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pydantic import BaseModel
from fastapi import Form

class LoginRequest(BaseModel):
    first_name: str = Form(..., max_length=30),
    last_name: str = Form(..., max_length=30),
    password: str = Form(..., max_length=30)
