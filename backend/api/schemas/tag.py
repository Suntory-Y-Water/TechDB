from typing import List

from pydantic import BaseModel, ConfigDict, Field, constr


class TagBase(BaseModel):
    """
    タグのベーススキーマ
    """

    tag_id: constr(min_length=1) = Field(..., example="Python")

    model_config = ConfigDict(from_attributes=True)


class TagsList(BaseModel):
    """
    タグのリストスキーマ
    """

    tags: List[TagBase]
