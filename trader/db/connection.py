import os
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncEngine, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from .models import Base


async def get_db_engine() -> tuple[AsyncEngine, async_sessionmaker[AsyncSession]]:
    engine = create_async_engine(os.environ.get('DATABASE_URL'), echo=True)

    # async_sessionmaker: a factory for new AsyncSession objects.
    # expire_on_commit - don't expire objects after transaction commit
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return engine, async_session

    # await insert_objects(async_session)
    # await select_and_update_objects(async_session)
    #
    # # for AsyncEngine created in function scope, close and
    # # clean-up pooled connections
    # await engine.dispose()
