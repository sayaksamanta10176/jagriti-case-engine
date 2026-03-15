import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from config import get_decrpted_values

db_user, db_pass, db_host, db_name = get_decrpted_values()

DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:5432/{db_name}"

engine = create_async_engine(DATABASE_URL, echo = False, future = True)

AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def get_session():
    async with AsyncSessionLocal() as session:
        yield session