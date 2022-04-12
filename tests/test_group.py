from vk_core.client import VkClient
from vk_core.group.group import VkGroup, VkGroupGetByIdQuery, VkGroupModel
from vk_core.tests.test_client import test_client_instance
from vk_core.wall.wall import *
import logging

client = test_client_instance()

logger = logging.getLogger(__name__)


def test_group_get_by_short_name ():
    group = VkGroup(
        client = client,
        group_id = "kf_films"
    )
    current_group: VkGroupModel = group.getById()
    # posts_response = wall.get(query = query)
    assert isinstance(current_group, VkGroupModel)
