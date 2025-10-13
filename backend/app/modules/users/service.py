from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password

from .models import User
from .repository import UserRepository
from .schemas import UserCreate


class UserService:
    """Business logic for user management."""

    def __init__(self, session: AsyncSession) -> None:
        self.repository = UserRepository(session)

    async def create_user(self, user_create: UserCreate) -> User:
        password_hash = hash_password(user_create.password)
        return await self.repository.create(user_create, password_hash)

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.repository.get_by_email(email)

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        return await self.repository.get_by_id(user_id)
