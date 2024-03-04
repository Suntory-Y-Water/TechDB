from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.blog as blog_model
import api.schemas.blog as blog_schma


async def create_blog(db: AsyncSession, blog_create: blog_schma.BlogCreate) -> blog_model.Blog:
    """新しいブログを作成する。"""
    blog = blog_model.Blog(**blog_create.model_dump())
    db.add(blog)
    await db.commit()
    await db.refresh(blog)
    return blog


async def get_all_blogs(db: AsyncSession) -> list[blog_model.Blog]:
    """全てのブログを取得する。"""
    result: Result = await db.execute(select(blog_model.Blog))
    blogs = result.scalars().all()
    return blogs


async def get_blog_by_id(db: AsyncSession, blog_id: str) -> blog_model.Blog | None:
    """ブログを取得する。"""
    result: Result = await db.execute(select(blog_model.Blog).filter(blog_model.Blog.id == blog_id))
    return result.scalars().first()


async def delete_blog(db: AsyncSession, blog_id: str) -> None:
    """指定されたIDのブログを削除する。"""
    query = select(blog_model.Blog).where(blog_model.Blog.id == blog_id)
    result: Result = await db.execute(query)
    blog_to_delete = result.scalar()

    if blog_to_delete:
        await db.delete(blog_to_delete)
        await db.commit()
