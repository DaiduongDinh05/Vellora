from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User
from .schemas import UserCreate


class UserRepository:
    """Data access layer for user entities."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, user_id: UUID) -> Optional[User]:
        stmt = select(User).where(User.id == user_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, user_create: UserCreate, password_hash: str) -> User:
        user = User(
            email=user_create.email,
            full_name=user_create.full_name,
            role=user_create.role,
            password_hash=password_hash,
        )
        self.session.add(user)
        await self.session.flush()
        return user
