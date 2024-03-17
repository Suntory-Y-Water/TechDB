from fastapi import APIRouter, Depends, Response, status
from fastapi import HTTPException

from api.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends
import api.cruds.tag as tag_crud
import api.schemas.tag as tag_schema

router = APIRouter()


@router.get("/api/tag", response_model=tag_schema.TagsList)
async def read_all_tags(db: AsyncSession = Depends(get_db)):
    """全てのタグを取得する"""
    tags = await tag_crud.get_all_tags(db)
    if tags is None:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return tags


@router.post("/api/tags", status_code=status.HTTP_201_CREATED)
async def create_tags(tags_body: tag_schema.TagsList, db: AsyncSession = Depends(get_db)):
    """複数のタグ情報を一括で追加する。既に存在する場合は更新する。"""
    try:
        await tag_crud.create_tags(db, tags_body.tags)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    return Response(status_code=status.HTTP_201_CREATED)