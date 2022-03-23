from vk_core.client import VkClient
from vk_core.group.group import Group, GroupGetByIdQuery, GroupModel
from vk_core.tests.test_client import test_client_instance
from vk_core.wall.wall import *
import logging

client = test_client_instance()

logger = logging.getLogger(__name__)


def test_group_get_by_short_name ():
    group = Group(
        client = client,
        group_id = "kf_films"
    )
    current_group: GroupModel = group.getById()
    # posts_response = wall.get(query = query)
    assert isinstance(current_group, GroupModel)
