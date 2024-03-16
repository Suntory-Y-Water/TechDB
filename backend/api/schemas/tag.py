from pydantic import BaseModel, Field, constr, ConfigDict
from typing import List

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