from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.settings import DB_HOST, DB_NAME, DB_PASSWORD, DB_USER


engine = create_async_engine(f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')
SessionLocal = async_sessionmaker(
    engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)


async def get_session():
    session = SessionLocal()

    try:
        yield session
    finally:
        await session.close()
