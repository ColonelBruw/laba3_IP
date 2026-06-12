# Добавляем текущую папку в sys.path для 
# корректного импорта зависимостей в другие файлы бекенда
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from pydantic import BaseModel
from fastapi import Form

class JobApplicationForm(BaseModel):
    pos: str = Form(..., max_length=30)
