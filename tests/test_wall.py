from vk_core.client import VkClient
from vk_core.tests.test_client import test_client_instance
from vk_core.wall.wall import *

client = test_client_instance()

def test_wall_get_posts():
    wall = VkWall(
        client = client,
        owner_id=-201355660,
        domain = 'opasnayapechenka',
    )
    posts_response = wall.get()
    assert isinstance(posts_response, WallPostsResponse)

