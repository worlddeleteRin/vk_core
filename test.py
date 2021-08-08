from vk_core import * 

new_client = {
	"api_v": 3.45,
	"api_url": "api.url.is.here",
	"not_existing_key": "some test value is here",
}

client = VkClient(**new_client)
print(client.__dict__)
print(client.api_v, client.api_url)
