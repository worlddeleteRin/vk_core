from pydantic import BaseModel
from typing import Any, Optional, Union

from httpx import Response

class BaseVkResponse(BaseModel):
    response: dict

class BaseVkErrorException(Exception):
    response: Optional[Response] = None
    error_code: Optional[Union[int, str]] = None
    error_msg: str

    def __init__(
        self,
        response: Response = None,
        error_code = None,
        error_msg: str = 'unknown error'
    ):
        self.response = response
        self.error_code = error_code
        self.error_msg = error_msg

    def raise_error(self):
        error =  f'{self.error_code} {self.error_msg}'
        if self.response:
            response_log = f'{self.response.json()}'
            request_log = f'{self.response.request}'
            error += f'{response_log} {request_log}'
        raise Exception(
            f'{error}'
        )

    @staticmethod
    def get_dummy_from_response(
        response: Response
    ):
        error = f'{response.json()}'
        response_log = f'{response.json()}'
        request_log = f'{response.request}'
        error += f'{response_log} {request_log}'
        return BaseVkErrorException(
            error_msg = error
        )
