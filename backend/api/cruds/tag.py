from datetime import datetime
from typing import List
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.dialects.mysql import insert as mysql_insert
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.tag as tag_model
import api.schemas.tag as tag_schema


async def get_all_tags(db: AsyncSession) -> tag_schema.TagsList:
    """全てのタグを取得する。"""
    try:
        result = await db.execute(select(tag_model.Tag.tag_id))
        tag_ids = result.scalars().all()

        tag_list: List[tag_schema.TagBase] = [tag_schema.TagBase(tag_id=tag_id) for tag_id in tag_ids]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return tag_schema.TagsList(tags=tag_list)


async def create_tags(db: AsyncSession, tags_create: List[tag_schema.TagBase]) -> None:
    """複数のタグを一括で作成する。既に存在する場合は更新時間を最新にする。"""
    try:
        for tag_create in tags_create:
            stmt = mysql_insert(tag_model.Tag).values(tag_id=tag_create.tag_id)
            stmt = stmt.on_duplicate_key_update(updated_at=datetime.now(ZoneInfo("Asia/Tokyo")))
            await db.execute(stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return None
