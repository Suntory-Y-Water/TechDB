from sqlalchemy import Column, String, DateTime, Table, ForeignKey
from datetime import datetime

from api.db import Base

article_tags_table = Table('article_tags', Base.metadata,
    Column('article_id', String(255), ForeignKey('articles.article_id'), primary_key=True),
    Column('tag_id', String(64), ForeignKey('tags.tag_id'), primary_key=True),
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
)