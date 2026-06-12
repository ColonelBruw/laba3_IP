# Помещаем в sys.path путь до директории server чтобы работали глобальные импорты
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import List, Optional
from model.db.dao.job_application_dao import JobApplicationDAO
from model.db.dao.user_dao import UserDAO
from model.core.security import decode_access_token
from model.schemas.job_application_form import JobApplicationForm
from model.db.db_base import JobApplication

# Установка локали (при развертывании через контейнер закоментировать)
# import locale
# try:
#     locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')
# except:
#     locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

class JobApplicationService:
    """Сервис для работы с заявками на работу"""
    
    def __init__(self, job_application_dao: JobApplicationDAO):
        self.job_application_dao = job_application_dao
    
    async def get_by_id(self, user_id: int) -> Optional[JobApplication]:
        job_application = await self.job_application_dao.get_by_id(user_id)
        if not job_application:
            return None
        return job_application
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[JobApplication]:
        job_applications = await self.job_application_dao.get_all(skip, limit)
        return job_applications
    
    async def create_application(self, application_form: JobApplicationForm, session_token: str) -> dict:
        applicant_id = decode_access_token(session_token).get('user_id')
        new_application = await self.job_application_dao.create_application(application_form.pos, applicant_id)
        
        await self.job_application_dao.session.commit()
        await self.job_application_dao.session.refresh(new_application)
        new_application_id = new_application.id

        return {
                'status': '200',
                'message': f'Заявка под номером {new_application_id} успешно заполнена!'
            }
    
    async def update_application(self, user_id: int, user_data: dict) -> Optional[JobApplication]:
        job_application = await self.job_application_dao.update_application(user_id, **user_data)
        if job_application:
            await self.job_application_dao.session.commit()
            return job_application
        return None
    
    async def delete_application(self, user_id: int) -> bool:
        result = await self.job_application_dao.delete_application(user_id)
        if result:
            await self.job_application_dao.session.commit()
        return result
    
    async def delete_all_applications(self) -> int:
        result = await self.job_application_dao.delete_all_applications()
        if result:
            await self.job_application_dao.session.commit()
        return result