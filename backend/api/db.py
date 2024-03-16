from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

ASYNC_DB_URL = "mysql+aiomysql://root@db:3306/tech-db?charset=utf8"
ASYNC_TEST_DB_URL = "mysql+aiomysql://root@db:3306/test_tech_db?charset=utf8"

async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_test_engine = create_async_engine(ASYNC_TEST_DB_URL, echo=True)

async_session = sessionmaker(autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession)
async_test_session = sessionmaker(autocommit=False, autoflush=False, bind=async_test_engine, class_=AsyncSession)

Base = declarative_base()

# DI用の関数を定義
async def get_db():
    async with async_session() as session:
        yield session

# テスト用のDI関数
async def get_test_db():
    async with async_test_session() as session:
        yield session