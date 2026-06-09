# Добавляем текущую папку в sys.path для 
# корректного импорта зависимостей в другие файлы бекенда

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Optional, List
from db_base import JobApplication

class JobApplicationDAO:
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, position_name: str, applicant_id: int) -> JobApplication:
        try:
            new_application = JobApplication(
                position_name=position_name,
                applicant_id=applicant_id
            )
            
            self.session.add(new_application)
            await self.session.commit()
            await self.session.refresh(new_application)
            
            return new_application
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def get_by_id(self, application_id: int) -> Optional[JobApplication]:
        try:
            result = await self.session.execute(
                select(JobApplication).filter(JobApplication.id == application_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def get_all(self) -> List[JobApplication]:
        try:
            result = await self.session.execute(select(JobApplication))
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def update(self, application_id: int, **kwargs) -> Optional[JobApplication]:
        try:
            application = await self.get_by_id(application_id)
            if not application:
                return None
            
            for field, value in kwargs.items():
                if hasattr(application, field):
                    setattr(application, field, value)
            
            await self.session.commit()
            await self.session.refresh(application)
            return application
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def delete(self, application_id: int) -> bool:
        try:
            application = await self.get_by_id(application_id)
            if not application:
                return False
            
            await self.session.delete(application)
            await self.session.commit()
            return True
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def delete_all(self) -> int:
        try:
            result = await self.session.execute(delete(JobApplication))
            await self.session.commit()
            return result.row_count
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e