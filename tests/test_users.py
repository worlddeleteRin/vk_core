import logging
from typing import Any
from vk_core.users.main import VkGetUsersQuery, VkUser, VkUserModel

from vk_core.likes.likes import AddLikeQuery, LikeTargetEnum, Likes

from .test_client import test_client_instance

logger = logging.getLogger(__name__)

client = test_client_instance()

test_user_ids = "worldedit505"
test_banned_user_id = "id136578416"

def test_get_user():
    query = VkGetUsersQuery(
        user_ids = test_user_ids
    )
    vk_users = VkUser(client = client).get(query = query)
    vk_user = vk_users[0]
    assert isinstance(vk_user, VkUserModel)

def test_not_banned():
    query = VkGetUsersQuery(
        user_ids = test_user_ids
    )
    vk_users = VkUser(client = client).get(query = query)
    vk_user = vk_users[0]
    assert vk_user.is_banned() == False

def test_banned():
    query = VkGetUsersQuery(
        user_ids = test_banned_user_id 
    )
    vk_users = VkUser(client = client).get(query = query)
    vk_user = vk_users[0]
    assert vk_user.is_banned() == True
