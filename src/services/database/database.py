from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from config.config import settings


engine = create_async_engine(
    settings.DATABASE_URL,
    echo=bool(settings._DEBUG),
)

async_session = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_session():
    async with async_session() as session:
        yield session