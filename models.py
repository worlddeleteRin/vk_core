from pydantic import BaseModel
from typing import Any, Optional, Union

from httpx import Response

class BaseVkResponse(BaseModel):
    response: Any

class BaseVkErrorException(Exception):
    response: Optional[Response] = None
    error_code: Optional[Union[int, str]] = None
    message: str

    def __init__(
        self,
        response: Optional[Response] = None,
        error_code = None,
        message: str = 'unknown error'
    ):
        self.response = response
        self.error_code = error_code
        self.message = message
        super().__init__(self.message)

    def raise_error(self):
        error =  f'{self.error_code} {self.message}'
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
        error = ''
        response_log = f'{response.json()}'
        request_log = f'{response.request}'
        error += f'{response_log} {request_log}'
        return BaseVkErrorException(
            response = response,
            message = error
        )

class BaseModelParseException(Exception):
    def __init__(
        self, 
        message: str = 'parse model exception'
    ):
        super().__init__(message)
