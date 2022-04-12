from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel
from httpx import Response

from vk_core.client import VkClient
from vk_core.likes.models import IsLikedResponse

class LikeTargetEnum(str, Enum):
    post = 'post'
    comment = 'comment'
    photo = 'photo'
    audio = 'audio'
    video = 'video'
    note = 'note'
    market = 'market'
    photo_comment = 'photo_comment'
    video_comment = 'video_comment'
    topic_comment = 'topic_comment'
    market_comment = 'market_comment'

class AddLikeQuery(BaseModel):
    type: LikeTargetEnum
    owner_id: int
    item_id: int
    # access_key for work with private objects
    access_key: Optional[str] = None
    class Config:
        use_enum_values = True

class IsLikedQuery(BaseModel):
    type: LikeTargetEnum
    owner_id: int
    item_id: int

    class Config:
        use_enum_values = True 

class Likes:
    client: VkClient

    def __init__(
        self,
        client
    ):
        self.client = client
        
    def isLiked(
        self,
        query: IsLikedQuery
    ) -> IsLikedResponse:
        resp: Response = self.client.http.client.get(
            'likes.isLiked',
            params = query.dict(exclude_none=True)
        )
        data = self.client.http.process_response(resp).response
        return IsLikedResponse.process_from_response(data)

    def add(
        self,
        query: AddLikeQuery,
    ) -> Any:
        resp: Response = self.client.http.client.get(
            'likes.add',
            params = query.dict(exclude_none=True)
        )
        data = self.client.http.process_response(resp).response
        return data


