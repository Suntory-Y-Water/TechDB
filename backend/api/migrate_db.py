from sqlalchemy import create_engine

from api.db import Base

from api.models.article import Article
from api.models.tag import Tag
from api.models.article_tags import article_tags_table

DB_URL = "mysql+pymysql://root@db:3306/tech-db?charset=utf8"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
