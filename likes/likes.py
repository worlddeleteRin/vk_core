from enum import Enum
from pydantic import BaseModel

LikeTargetEnum(str, Enum):
    post = 'post'
    comment = 'comment'
    photo = 'photo'
    audio = 'audio'
    video = 'video'
    note = 'note'
    market = 'market'
    photo_comment = 'photo_comment'

class AddLikeQuery(BaseModel):
    type: LikeTargetEnum


class Likes:
    def add(
        self,
        query: AddLikeQuery,
    ):
