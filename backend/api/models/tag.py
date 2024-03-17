from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime
from datetime import datetime
from zoneinfo import ZoneInfo
from api.models.article import Article
from api.models.article_tags import article_tags_table


from api.db import Base

class Tag(Base):
    __tablename__ = "tags"
    tag_id = Column(String(64), primary_key=True)
    updated_at = Column(DateTime, default=lambda: datetime.now(ZoneInfo("Asia/Tokyo")))
    articles = relationship("Article", secondary=article_tags_table, back_populates="tags")
