from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, Integer, UnicodeText
from datetime import datetime
from api.models.article_tags import article_tags_table

from api.db import Base

class Article(Base):
    __tablename__ = "articles"
    article_id = Column(String(255), primary_key=True)
    title = Column(String(255), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    likes_count = Column(Integer, nullable=False, default=0)
    stocks_count = Column(Integer, nullable=False, default=0)
    read_time = Column(Integer, nullable=False, default=60)
    url = Column(String(255), nullable=False)
    source = Column(String(1), nullable=False, default='1')
    ogp_image_url = Column(UnicodeText, nullable=False)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    tags = relationship("Tag", secondary=article_tags_table, back_populates="articles")

