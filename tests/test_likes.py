import logging
from typing import Any

from vk_core.likes.likes import AddLikeQuery, LikeTargetEnum, Likes

from .test_client import test_client_instance

logger = logging.getLogger(__name__)

client = test_client_instance()


# test_post_id = "-201355660_15259"
test_wall_id = -201355660
test_post_id = 15259

def test_like_post():
    query = AddLikeQuery(
        type = LikeTargetEnum.post,
        owner_id = test_wall_id,
        item_id = test_post_id
    )
    likes = Likes(client = client)
    data: Any = likes.add(query = query)
    logger.warning(f'data is {data}')
    return data

