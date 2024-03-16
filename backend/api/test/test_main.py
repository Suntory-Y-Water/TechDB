import pytest
import pytest_asyncio
import starlette.status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from api.db import get_test_db, Base, ASYNC_TEST_DB_URL
from api.main import app

@pytest_asyncio.fixture(autouse=True)
async def setup_and_teardown():
    # テスト用のengineとsessionを作成
    async_test_engine = create_async_engine(ASYNC_TEST_DB_URL)
    async_test_session = sessionmaker(autocommit=False, autoflush=False, bind=async_test_engine, class_=AsyncSession)

    # テスト前にテーブルを削除し、再作成する
    async with async_test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # テスト用のDI関数を定義
    async def get_test_db_with_session():
        async with async_test_session() as session:
            yield session

    # DIを使ってFastAPIのDBの向き先をテスト用DBに変更
    app.dependency_overrides[get_test_db] = get_test_db_with_session

    yield

    # テスト後にテーブルを削除する
    async with async_test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # テスト終了後にDIを解除
    app.dependency_overrides.pop(get_test_db)

    # テスト用のengineとsessionを閉じる
    await async_test_engine.dispose()

@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    # テスト用に非同期HTTPクライアントを返却
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_tags(async_client: AsyncClient):
    # タグの作成
    tags = [{"tag_id": "Python"}, {"tag_id": "FastAPI"}]
    response = await async_client.post("/api/tags", json={"tags": tags})
    assert response.status_code == starlette.status.HTTP_201_CREATED