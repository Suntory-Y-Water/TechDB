from fastapi import APIRouter, Depends, status
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.db import get_db
import api.schemas.article as article_schema
import api.cruds.article as article_crud

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
