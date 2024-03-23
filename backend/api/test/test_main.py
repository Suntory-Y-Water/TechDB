from datetime import datetime, timedelta

import pytest
import pytest_asyncio
import starlette.status
from httpx import AsyncClient

from api.db import Base, async_test_engine, get_db, get_test_db
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


@pytest.mark.asyncio
async def test_get_qiita_trend(async_client: AsyncClient):
    # 2024/03/23時点のトレンドが存在しないため、2024/03/22時点のトレンドを取得
    created_at = datetime.now().date() - timedelta(days=1)
    tag = "Python"

    # エンドポイントの応答を確認
    response = await async_client.get(f"/api/articles/qiita?created_at={created_at}&tag={tag}")
    assert response.status_code == starlette.status.HTTP_200_OK

    # レスポンスデータの構造を確認
    data = response.json()
    assert "articles" in data
    assert isinstance(data["articles"], list)

    # クエリパラメータの動作を確認
    for article in data["articles"]:
        assert article["created_at"] >= created_at.isoformat()
        assert tag in [tag["tag_id"] for tag in article["tags"]]

    # 記事データの正確性を確認
    for article in data["articles"]:
        assert "article_id" in article
        assert "title" in article
        assert "likes_count" in article
        assert "url" in article
        assert "source" in article
        assert "ogp_image_url" in article
        assert "created_at" in article
        assert "stocks_count" in article
        assert "read_time" in article
        assert "tags" in article

    # バリデーションエラーの処理を確認
    response = await async_client.get(f"/api/articles/qiita?created_at=20240323&tag={tag}")
    assert response.status_code == starlette.status.HTTP_422_UNPROCESSABLE_ENTITY

    # 意味不明なクエリパラメータを指定したときの処理を確認
    response = await async_client.get("/api/articles/qiita?creafsdfsted_at=invalid_date&tafadsfdasg=")
    assert response.status_code == starlette.status.HTTP_500_INTERNAL_SERVER_ERROR

    # エッジケースの処理を確認
    response = await async_client.get("/api/articles/qiita?created_at=2000-01-01&tag=NonExistentTag")
    assert response.status_code == starlette.status.HTTP_200_OK
    data = response.json()
    assert len(data["articles"]) == 0  # 記事が存在しない場合は空のリストが返ることを確認


@pytest.mark.asyncio
async def test_create_and_read_qiita_trend(async_client: AsyncClient):
    # 2024/03/23時点のトレンドが存在しないため、2024/03/22時点のトレンドを取得
    created_at = datetime.now().date() - timedelta(days=1)
    tag = "Python"

    # 前段階としてタグを作成しておく
    tags = [
        {"tag_id": "Python"},
        {"tag_id": "FastAPI"},
        {"tag_id": "AWS"},
        {"tag_id": "lambda"},
        {"tag_id": "bedrock"},
        {"tag_id": "AWS"},
        {"tag_id": "RDKit"},
        {"tag_id": "Smiles"},
        {"tag_id": "ChatGPT"},
        {"tag_id": "RDLogger"},
        {"tag_id": "tips"},
        {"tag_id": "tool"},
        {"tag_id": "QRコード"},
    ]
    # タグを作成
    response = await async_client.post("/api/tags", json={"tags": tags})
    assert response.status_code == starlette.status.HTTP_201_CREATED

    # qiitaからトレンド記事を取得
    response = await async_client.get(f"/api/articles/qiita?created_at={created_at}&tag={tag}")
    assert response.status_code == starlette.status.HTTP_200_OK
    articles = response.json()

    # 取得したトレンド記事を登録
    response = await async_client.post("/api/articles", json=articles)
    assert response.status_code == starlette.status.HTTP_201_CREATED
