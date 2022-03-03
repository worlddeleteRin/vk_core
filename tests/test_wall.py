from vk_core.client import VkClient
from vk_core.tests.test_client import test_client_instance
from vk_core.wall.wall import *
import logging

client = test_client_instance()

logger = logging.getLogger(__name__)


def test_wall_get_posts():
    wall = VkWall(
        client = client,
        # owner_id=-201355660,
        domain = 'opasnayapechenka',
    )
    query = WallPostsGetQuery(
        count = 1
    )
    posts_response = wall.get(query = query)
    assert isinstance(posts_response, WallPostsResponse)
