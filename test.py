from vk_core import * 

new_client = {
	"api_v": 3.45,
	"api_url": "api.url.is.here",
	"access_token": "some_access_token_is_here",
}

client = VkClient(**new_client)
print(client.__dict__)
print(client.api_v, client.api_url)
