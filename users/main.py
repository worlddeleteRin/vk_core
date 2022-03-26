from typing import Optional
from pydantic.main import BaseModel
from .enums import DeactivatedEnum
from vk_core.client import VkClient
from httpx import Response

from vk_core.models import BaseModelParseException

class VkUserModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    deactivated: Optional[str] = None
    is_closed: Optional[bool] = None
    can_access_closed: Optional[bool] = None
    # TODO add optional fields

    def is_banned(self) -> bool:
        d = self.deactivated
        if not d:
            return False
        if (
            (d == DeactivatedEnum.deleted) or
            (d == DeactivatedEnum.banned)
        ):
            return True
        return False
            

class VkGetUsersQuery(BaseModel):
    # string of users ids seprated by ,
    user_ids: Optional[str] = None
    # optional fields to return
    # TODO: make enum?
    fields: Optional[str] = None

    class Config:
        allow_population_by_field_name = True

class VkUser(
):
    client: VkClient

    def __init__(
        self,
        client: VkClient
    ):
        self.client = client
    
    """
    Get user(s) info
    """
    def get(
        self,
        query: VkGetUsersQuery = VkGetUsersQuery()
    ):
        resp_raw: Response = self.client.http.client.get(
            url = 'users.get',
            params = query.dict(exclude_none=True)
        )
        resp: dict = self.client.http.process_response(resp_raw).response
        if not isinstance(resp, list):
            raise BaseModelParseException()
        users = [VkUserModel(**user) for user in resp]
        return users
