from typing import Any, NewType, Optional
from pydantic import BaseModel
from vk_core.client import VkClient
from httpx import Response
from vk_core.models import BaseModelParseException, BaseVkErrorException, BaseVkResponse

class VkPost(BaseModel):
    id: int
    # identifier of the wall owner
    owner_id: int
    # post author id
    from_id: int
    created_by: Optional[int] = None
    # date in unixtime
    date: int
    # post body text
    text: str   
    reply_owner_id: Optional[int]
    reply_post_id: Optional[int]
    friends_only: Optional[int]
    comments: dict
    copyright: Optional[dict]
    likes: dict
    reposts: dict
    views: Optional[dict]
    # TODO: add enum
    post_type: str
    post_source: dict
    attachments: list = []
    geo: Optional[dict]
    signer_id: Optional[int]
    copy_history: list = []
    can_pin: Optional[int]
    can_delete: Optional[int]
    can_edit: Optional[int]
    is_pinned: Optional[int]
    marked_as_ads: int
    is_favorite: bool
    donut: dict
    # if of scheduled post if it was scheduled
    postponed_id: Optional[int] = None

# request & responses 
class WallPostGetByIdQuery(BaseModel):
    # string of posts ids
    # 93388_21539,93388_20904,-1_340364
    posts: str
    extended: int = 0
    # depth of copy_history array, if post is replied
    copy_history_depth: int = 1
    fields: Optional[str] = None


class WallPostsGetQuery(BaseModel):
    owner_id: Optional[int] = None
    domain: Optional[str] = None
    filter: Optional[str] = None
    offset: int = 0
    count: int = 5
    extended: int = 0
    fields: Optional[str] = None

class WallPostsResponse(BaseModel):
    count: int
    items: list[VkPost]

    @staticmethod
    def process_from_response(resp: Any):
        parse_exception = BaseModelParseException(
            'WallPostsResponse parse error'
        )
        if not isinstance(resp, dict):
            raise parse_exception

        return WallPostsResponse(
            **resp
        )

# eof request & responses

class VkWall():
    client: VkClient
    owner_id: Optional[int] = None
    domain: Optional[str] = None

    def __init__(
        self,
        client,
        owner_id: int | None = None,
        domain: str | None = None
    ):
        self.client = client
        if (owner_id is None) and (domain is None):
            raise Exception('specify owner_id or domain')
        self.owner_id = owner_id
        self.domain = domain

    @staticmethod
    def getOwnerItemIdsFromUrl(url: str) -> list[str] | None:
        s = url.split('wall')
        if len(s) < 2:
            return None
        items = s[1].split('_')
        if len(items) < 2:
            return None
        return items

    def get(
        self,
        query: WallPostsGetQuery = WallPostsGetQuery()
    ) -> WallPostsResponse:
        if self.owner_id is not None:
            query.owner_id = self.owner_id
        elif self.domain is not None: 
            query.domain = self.domain

        resp_raw: Response = self.client.http.client.get(
            url = '/wall.get',
            params = query.dict(exclude_none=True)
        )

        resp = self.client.http.process_response(resp_raw).response

        data = WallPostsResponse.process_from_response(resp)
        return data

    def getById(
        self,
        query: WallPostGetByIdQuery
    ) -> list[VkPost]:
        resp_raw: Response = self.client.http.client.get(
            url = 'wall.getById',
            params = query.dict(exclude_none=True)
        )
        resp: dict = self.client.http.process_response(resp_raw).response
        if not isinstance(resp, list):
            raise BaseModelParseException()

        data = [VkPost(**post) for post in resp]
        return data



