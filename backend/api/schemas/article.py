import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, constr

from .tag import TagBase


class ArticleBase(BaseModel):
    article_id: constr(min_length=1) = Field(..., example="8524fe3a22a2faa47b7a")
    title: constr(min_length=1) = Field(
        ..., example="牛乳を1つ買ってきてください。卵があったら6つ買ってきてください。のような仕様書"
    )
    likes_count: int = Field(0, example=0)
    url: constr(min_length=1) = Field(..., example="https://qiita.com/SZR/items/8524fe3a22a2faa47b7a")
    source: constr(min_length=1) = Field(..., example="1", description="1: Qiita, 2: Zenn")
    ogp_image_url: Optional[str] = Field(None, example="https://example.com/ogp_image.png")
    created_at: datetime.datetime = Field(..., example="2024-01-15T13:07:45.208Z")


class Article(ArticleBase):
    stocks_count: int = Field(0, example=0)
    read_time: int = Field(0, example=5)
    tags: List[TagBase] = Field(..., example=[{"tag_id": "Python"}, {"tag_id": "FastAPI"}])


class ArticleCreate(Article):
    pass


class ArticleCreateRequest(BaseModel):
    articles: List[ArticleCreate]


class ArticleResponse(Article):
    model_config = ConfigDict(from_attributes=True)


class ArticleListResponse(BaseModel):
    articles: List[ArticleResponse]
