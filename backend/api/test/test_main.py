import pytest
import pytest_asyncio
import starlette.status
from httpx import AsyncClient
from api.db import get_db, get_test_db, Base, async_test_engine
from api.main import app


@pytest_asyncio.fixture(autouse=True)
async def setup_and_teardown():
    app.dependency_overrides[get_db] = get_test_db
    async with async_test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with async_test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    app.dependency_overrides.clear()
    await async_test_engine.dispose()


@pytest_asyncio.fixture
async def async_client() -> AsyncClient:
    # テスト用に非同期HTTPクライアントを返却
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
async def test_create_and_read_tags(async_client: AsyncClient):
    # タグの作成
    tags = [{"tag_id": "Python"}, {"tag_id": "FastAPI"}]
    response = await async_client.post("/api/tags", json={"tags": tags})
    assert response.status_code == starlette.status.HTTP_201_CREATED
    response = await async_client.get("/api/tag")
    assert response.status_code == starlette.status.HTTP_200_OK
    data = response.json()
    assert len(data["tags"]) == 2
    assert {"tag_id": "Python"} in data["tags"]
    assert {"tag_id": "FastAPI"} in data["tags"]


@pytest.mark.asyncio
async def test_create_and_read_articles(async_client: AsyncClient):
    # 前段階としてタグを作成しておく
    tags = [{"tag_id": "Python"}, {"tag_id": "FastAPI"}]
    response = await async_client.post("/api/tags", json={"tags": tags})
    assert response.status_code == starlette.status.HTTP_201_CREATED

    # 記事の作成
    articles = [
        {
            "article_id": "8524fe3a22a2faa47b7a",
            "title": "牛乳を1つ買ってきてください。卵があったら6つ買ってきてください。のような仕様書",
            "likes_count": 0,
            "stocks_count": 0,
            "read_time": 0,
            "url": "https://qiita.com/SZR/items/8524fe3a22a2faa47b7a",
            "source": "1",
            "ogp_image_url": "https://example.com/ogp_image.png",
            "created_at": "2024-01-15T13:07:45.208Z",
            "tags": [{"tag_id": "Python"}, {"tag_id": "FastAPI"}],
        },
        {
            "article_id": "123456",
            "title": "牛乳を1つ買ってきてください。卵があったら6つ買ってきてください。のような仕様書",
            "likes_count": 0,
            "stocks_count": 0,
            "read_time": 0,
            "url": "https://qiita.com/SZR/items/123456",
            "source": "1",
            "ogp_image_url": "https://example.com/ogp_image.png",
            "created_at": "2024-01-15T13:07:45.208Z",
            "tags": [{"tag_id": "Python"}, {"tag_id": "FastAPI"}],
        },
    ]
    response = await async_client.post("/api/articles", json={"articles": articles})
    assert response.status_code == starlette.status.HTTP_201_CREATED
    response = await async_client.get("/api/articles")
    assert response.status_code == starlette.status.HTTP_200_OK
    data = response.json()
    # レスポンスのデータ構造の確認
    assert len(data["articles"]) == 2
