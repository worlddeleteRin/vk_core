
from typing import Any, Optional
from pydantic.main import BaseModel
from vk_core.client import VkClient
from vk_core.group.exceptions import GroupNotFoundException
from vk_core.models import BaseModelParseException
from httpx import Response

class GroupGetByIdQuery(BaseModel):
    # groups ids/short names separated by comma
    groups_ids: Optional[str] = None
    group_id: str

class GroupModel(BaseModel):
    id: int
    name: str
    screen_name: str
    is_closed: int
    # TODO: transform to enum with avail. values
    deactivated: Optional[str]
    is_admin: Optional[int]
    admin_level: Optional[int]
    is_member: Optional[int]
    is_advertiser: Optional[int]
    invited_by: Optional[int]
    # TODO: convert to enum
    type: Optional[str]
    # group main image with 50x50
    photo_50: str
    # group main image with 100x100
    photo_100: str
    # group main image with max res.
    photo_200: str

    @staticmethod
    def process_from_response(resp: Any):
        parse_exception = BaseModelParseException(
            f'Group model parse error {resp}'
        )
        if not isinstance(resp, dict):
            raise parse_exception

        return GroupModel(
            **resp
        )


class Group():
    client: VkClient
    group_id: str

    def __init__(
        self,
        client: VkClient,
        group_id: str
    ):
        self.client = client
        self.group_id = group_id

    def getById(
        self,
        query: Optional[GroupGetByIdQuery] = None
    ):
        if not query:
            query = GroupGetByIdQuery(
                group_id = self.group_id
            )
        resp_raw: Response = self.client.http.client.get(
            url = 'groups.getById',
            params = query.dict(exclude_none=True)
        )
        resp: dict = self.client.http.process_response(resp_raw).response
        if not isinstance(resp, list):
            raise BaseModelParseException()
        # TODO: mb add process from response
        groups = [GroupModel.process_from_response(g) for g in resp]
        if len(groups) == 0:
            raise GroupNotFoundException()
        return groups[0]
