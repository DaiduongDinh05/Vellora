from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import hash_password

from .models import User, UserRole
from .repository import UserRepository
from .schemas import UserCreate


class UserService:
    """Business logic for user management."""

    def __init__(self, session: AsyncSession) -> None:
        self.repository = UserRepository(session)

    async def create_user(self, user_create: UserCreate) -> User:
        password_hash = hash_password(user_create.password)
        return await self.repository.create(user_create, password_hash)

    async def ensure_user_for_oauth(
        self,
        email: str,
        full_name: str | None,
        role: UserRole = UserRole.EMPLOYEE,
    ) -> User:
        existing = await self.repository.get_by_email(email)
        if existing:
            return existing
        return await self.repository.create_oauth_user(email=email, full_name=full_name, role=role)

    async def get_by_email(self, email: str) -> Optional[User]:
        return await self.repository.get_by_email(email)

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        return await self.repository.get_by_id(user_id)
