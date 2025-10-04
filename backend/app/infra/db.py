from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=True)
AsyncsessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db():
    async with AsyncsessionLocal() as session:
        yield session