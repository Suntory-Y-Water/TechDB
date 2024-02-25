from api.db import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Response, status
import api.cruds.blog as blog_crud
import api.schemas.blog as schema

router = APIRouter()


@router.get("/blog", response_model=list[schema.Blog])
async def read_all_blogs(db: AsyncSession = Depends(get_db)):
    """
    ブログを全件取得する
    """
    return await blog_crud.get_all_blogs(db)


@router.get("/blog/{blog_id}", response_model=schema.Blog)
async def read_blog(blog_id: str, db: AsyncSession = Depends(get_db)):
    """
    個別のブログを取得する
    """
    blog = await blog_crud.get_blog_by_id(db, blog_id)
    if blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog


@router.post("/blog", response_model=schema.BlogCreateResponse)
async def create_blog(blog_body: schema.BlogCreate, db: AsyncSession = Depends(get_db)):
    """
    ブログを作成する
    """
    return await blog_crud.create_blog(db, blog_body)


@router.delete("/blog/{blog_id}", response_model=None)
async def delete_blog(blog_id: str, db: AsyncSession = Depends(get_db)):
    """
    ブログを削除する。
    """
    existing_blog = await blog_crud.get_blog_by_id(db, blog_id)
    if existing_blog is None:
        raise HTTPException(status_code=404, detail="Blog not found")

    # 存在する場合は削除を実行
    await blog_crud.delete_blog(db, blog_id)

    # 削除が成功したことを示すHTTPステータスコードを返す
    return Response(status_code=status.HTTP_204_NO_CONTENT)
