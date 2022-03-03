from typing import Optional
from pydantic import BaseModel
from vk_core.client import VkClient
from httpx import Response
from vk_core.models import BaseVkError, BaseVkResponse

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
# eof request & responses

class VkWall():
    client: VkClient
    owner_id: Optional[int] = None
    domain: Optional[str] = None

    def __init__(
        self,
        client,
        owner_id: int = None,
        domain: str = None
    ):
        self.client = client
        if (owner_id is None) and (domain is None):
            raise Exception('specify owner_id or domain')
        self.owner_id = owner_id
        self.domain = domain

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
        resp = self.client.http.process_response(resp_raw)
        if isinstance(resp, BaseVkError):
            resp.raise_error()
        if isinstance(resp, BaseVkResponse):
            resp_data = resp.response
            if isinstance(resp_data, dict):
                data = WallPostsResponse(
                    **resp_data
                )
                return data
        raise Exception('unhandled error while getting posts')

    def getById(
        self
    ):
        pass

