from vk_core.client import VkClient
from vk_core.tests.test_client import test_client_instance
from vk_core.wall.wall import *
import logging

client = test_client_instance()

logger = logging.getLogger(__name__)

wall = VkWall(
    client = client,
    # owner_id=-201355660,
    domain = 'opasnayapechenka',
)

def test_wall_get_posts():
    query = WallPostsGetQuery(
        count = 1
    )
    posts_response = wall.get(query = query)
    assert isinstance(posts_response, WallPostsResponse)

def test_wall_get_by_id():
    query = WallPostGetByIdQuery(
        posts = "-201355660_15259"
    )
    posts = wall.getById(query)
    if len(posts) == 0:
        raise Exception('no posts found')
    assert isinstance(posts[0], VkPost)
