from typing import List
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.mysql import insert as mysql_insert

import api.models.article as article_model
import api.models.tag as tag_model
import api.schemas.tag as tag_schema
import api.schemas.article as article_schema

from datetime import datetime
from zoneinfo import ZoneInfo


async def create_articles_with_tags(db: AsyncSession, articles_create: List[article_schema.ArticleCreate]) -> None:
    """新しい記事を作成する。紐づくタグ情報も同時に作成する。"""
    try:
        for article_create in articles_create:
            tags = []
            for tag_data in article_create.tags:
                tag = await db.scalar(select(tag_model.Tag).where(tag_model.Tag.tag_id == tag_data.tag_id))
                if tag is None:
                    tag = tag_model.Tag(tag_id=tag_data.tag_id)
                    db.add(tag)
                tags.append(tag)

            article_data = article_create.model_dump(exclude={"tags"})
            article_data["updated_at"] = datetime.now(ZoneInfo("Asia/Tokyo"))

            stmt = mysql_insert(article_model.Article).values(**article_data)
            do_update_stmt = stmt.on_duplicate_key_update(updated_at=datetime.now(ZoneInfo("Asia/Tokyo")))
            await db.execute(do_update_stmt)

        await db.commit()
    except Exception as e:
        print(f"記事の作成に失敗しました。: {str(e)}")
        await db.rollback()
        raise


async def get_articles(db: AsyncSession) -> List[article_schema.ArticleResponse]:
    """記事一覧を取得する。"""
    try:
        result = await db.execute(select(article_model.Article).options(selectinload(article_model.Article.tags)))
        articles = result.scalars().all()
        articles_response = []
        for article in articles:
            # モデル変換
            tags_converted = [tag_schema.TagBase.model_validate(tag) for tag in article.tags]
            article_response = article_schema.ArticleResponse.model_validate(article)

            article_response.tags = tags_converted
            articles_response.append(article_response)
        return articles_response
    except Exception as e:
        print(f"記事の取得に失敗しました: {str(e)}")
        raise
