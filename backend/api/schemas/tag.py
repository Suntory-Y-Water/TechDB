from typing import List

from pydantic import BaseModel, ConfigDict, Field, constr
from pydantic.alias_generators import to_camel


class TagBase(BaseModel):
    """
    タグのベーススキーマ
    """

    tag_id: constr(min_length=1) = Field(..., example="Python")

    model_config = ConfigDict(from_attributes=True)


class TagRespose(TagBase):
    model_config = ConfigDict(from_attributes=True, alias_generator=to_camel, populate_by_name=True)


class TagsList(BaseModel):
    """
    タグのリストスキーマ
    """

    tags: List[TagBase]


class TagsListResponse(BaseModel):
    tags: List[TagRespose]
