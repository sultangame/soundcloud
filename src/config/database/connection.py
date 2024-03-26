from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from dotenv import load_dotenv
import os


load_dotenv()
username = os.environ.get("POSTGRES_USER")
password = os.environ.get("POSTGRES_PASSWORD")
host = os.environ.get("POSTGRES_HOST")
db = os.environ.get("POSTGRES_DB")


async_url = f"postgresql+asyncpg://{username}:{password}@{host}/{db}"
async_engine = create_async_engine(url=async_url)
async_session_factory = async_sessionmaker(async_engine)


async def get_async_session():
    async with async_session_factory() as session:
        yield session
