# from main.client import *
from vk_core.client import *

def test_client_instance():
    client_config = {
        'access_token': 'd5bb144065d60759e1eabbc01ee3ef0ff90ef8dd6b05a681e5c717ac60d7a872fa4b4a080a33d68a3f9cbk'
    }
    client = VkClient(**client_config)
    assert isinstance(client, VkClient)
    return client
