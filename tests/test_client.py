# from main.client import *
from vk_core.main.client import *

def test_client_instance():
    client_config = {
        'access_token': 'some test token here'
    }
    client = VkClient(**client_config)
    return client is Client
