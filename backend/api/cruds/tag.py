from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.dialects.mysql import insert as mysql_insert
from datetime import datetime
from zoneinfo import ZoneInfo

import api.models.tag as tag_model
import api.schemas.tag as tag_schema

async def get_all_tags(db: AsyncSession) -> tag_schema.TagsList:
    """全てのタグを取得する。"""
    try:
        result = await db.execute(select(tag_model.Tag.tag_id))
        tag_ids = result.scalars().all()

        tag_bases: List[tag_schema.TagBase] = [tag_schema.TagBase(tag_id=tag_id) for tag_id in tag_ids]
        tags_list = tag_schema.TagsList(tags=tag_bases)

        return tags_list
    except SQLAlchemyError as e:
        print(f"タグの取得に失敗しました: {str(e)}")
        raise

async def create_tags(db: AsyncSession, tags_create: List[tag_schema.TagBase]) -> None:
    """複数のタグを一括で作成する。既に存在する場合は更新時間を最新にする。"""
    try:
        for tag_create in tags_create:
            stmt = mysql_insert(tag_model.Tag).values(
                tag_id=tag_create.tag_id
            )
            stmt = stmt.on_duplicate_key_update(
                updated_at=datetime.now(ZoneInfo("Asia/Tokyo"))
            )
            await db.execute(stmt)
        await db.commit()
    except SQLAlchemyError as e:
        print(f"タグの作成または更新に失敗しました: {str(e)}")
        await db.rollback()
        raise