import requests
import json
import time

from httpx import Client, Response

from vk_core.models import BaseVkErrorException, BaseVkResponse

class HttpModule():
    is_debug: bool = True
    client: Client 

    def __init__(
        self,
        client: Client
    ):
        self.client = client

    def process_response (
        self,
        response: Response
    ) -> BaseVkResponse:
        response_dict = dict(response.json())
        if response.status_code != 200:
            response_error = response_dict.get('error')
            if isinstance(response_error, dict):
                error = BaseVkErrorException(
                    response = response,
                    **response_error 
                )
            else:
                error = BaseVkErrorException.get_dummy_from_response(
                    response
                )
            raise error
        response_success = response_dict.get('response')
        if not isinstance(response_success, dict):
            raise BaseVkErrorException.get_dummy_from_response(response)
        else:
            return BaseVkResponse(
                response = response_success
            )
        

class VkClient():
    http: HttpModule
    access_token: str
    api_v: str
    api_url: str
    app_id: int

    def __init__(self,
            access_token: str,
            api_v: str = '5.131',
            api_url: str = 'https://api.vk.com/method',
            app_id: int = 7709111
        ):
        self.api_v = api_v
        self.api_url = api_url
        self.access_token = access_token
        # init httpx Client
        self.http = HttpModule(
            client = Client(
                base_url = self.api_url,
                params = {
                    'access_token': self.access_token,
                    'v': self.api_v
                }
            )
        )


    def request_token_url(self, app_id=7709111):
        return f'https://oauth.vk.com/authorize?client_id={app_id}&redirect_uri=https://oauth.vk.com/blank.html&display=popup&scope=notify+friends+photos+status+wall+offline+groups+stats+email+market&response_type=token&revoke=1'
