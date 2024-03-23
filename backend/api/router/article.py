import datetime
import os

import requests
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.article as article_crud
import api.schemas.article as article_schema
from api.db import get_db
from api.services.article_service import calculate_reading_time, get_qiita_ogp_image_url, remove_special_characters

router = APIRouter()


@router.post("/api/articles", status_code=status.HTTP_201_CREATED)
async def create_articles(articles_body: article_schema.ArticleCreateRequest, db: AsyncSession = Depends(get_db)):
    """
    複数の記事情報を一括で追加する。
    """
    try:
        await article_crud.create_articles_with_tags(db, articles_body.articles)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return None


@router.get("/api/articles", response_model=article_schema.ArticleListResponse)
async def get_articles(db: AsyncSession = Depends(get_db)):
    """全ての記事を取得する"""
    try:
        articles = await article_crud.get_articles(db)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return article_schema.ArticleListResponse(articles=articles)


@router.get("/api/articles/qiita", response_model=article_schema.ArticleListResponse)
async def get_qiita_trend(
    created_at: datetime.date = Query(None, description="記事の作成日"),
    tag: str = Query(None, description="記事のタグ"),
):
    """Qiitaの記事から特定のタグと作成日でフィルタされた記事を取得する"""
    try:
        load_dotenv()
        QIITA_API_URL = os.getenv("QIITA_API_URL")
        QIITA_ACCESS_TOKEN = os.getenv("QIITA_ACCESS_TOKEN")
        params = {
            "page": 1,
            "per_page": 20,
            "query": f"tag:{tag} created:>{created_at}",
        }
        response = requests.get(
            f"{QIITA_API_URL}/items", params=params, headers={"Authorization": f"Bearer {QIITA_ACCESS_TOKEN}"}
        )
        data = response.json()

        articles = []
        for item in data:
            article = article_schema.Article(
                article_id=item["id"],
                title=remove_special_characters(item["title"]),
                likes_count=item["likes_count"],
                url=item["url"],
                source="1",
                ogp_image_url=get_qiita_ogp_image_url(item["url"]),
                created_at=item["created_at"],
                stocks_count=item["stocks_count"],
                read_time=calculate_reading_time(item["body"]),
                tags=[article_schema.TagBase(tag_id=tag["name"]) for tag in item["tags"]],
            )
            articles.append(article)

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return article_schema.ArticleListResponse(articles=articles)
