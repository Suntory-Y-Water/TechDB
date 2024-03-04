from sqlalchemy import Column, String, DateTime, CHAR
import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from api.db import Base

class Blog(Base):
    __tablename__ = "blog"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(1024))
    content = Column(String(1024))
    createdAt = Column(DateTime, default=lambda: datetime.now(ZoneInfo("Asia/Tokyo")))