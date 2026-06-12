# Добавляем текущую папку в sys.path для 
# корректного импорта зависимостей в другие файлы бекенда

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from typing import Optional, List
from model.db.db_base import User

class UserDAO:
    
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create_user(self, first_name: str, last_name: str, password: str,
                     phone_number: Optional[str] = None, 
                     email: Optional[str] = None) -> Optional[User]:
        try:
            new_user = User(
                first_name=first_name,
                last_name=last_name,
                phone_number=phone_number,
                email=email,
                password=password
            )
            self.session.add(new_user)

            return new_user
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        try:
            result = await self.session.execute(
                select(User).filter(User.id == user_id)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def get_all(self) -> List[User]:
        try:
            result = await self.session.execute(select(User))
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def get_by_email(self, email: str) -> Optional[User]:
        try:
            result = await self.session.execute(
                select(User).filter(User.email == email)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def get_by_phone(self, phone_number: str) -> Optional[User]:
        try:
            result = await self.session.execute(
                select(User).filter(User.phone_number == phone_number)
            )
            return result.scalar_one_or_none()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def get_by_name(self, first_name: str, last_name: str) -> List[User]:
        try:
            result = await self.session.execute(
                select(User).filter(User.first_name == first_name,
                                    User.last_name == last_name)
            )
            return result.scalars().all()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def update_user(self, user_id: int, **kwargs) -> Optional[User]:
        try:
            user = await self.get_by_id(user_id)
            if not user:
                return None
            
            for field, value in kwargs.items():
                if hasattr(user, field):
                    setattr(user, field, value)
        
            return user
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def delete_user(self, user_id: int) -> bool:
        try:
            user = await self.get_by_id(user_id)
            if not user:
                return False
            
            await self.session.delete(user)
            return True
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e
    
    async def delete_all_users(self) -> int:
        try:
            result = await self.session.execute(delete(User))
            return result.rowcount
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e