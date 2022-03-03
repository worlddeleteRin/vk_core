from pydantic import BaseModel
from typing import Any, Optional, Union

from httpx import Response

class BaseVkResponse(BaseModel):
    response: Any

class BaseVkError(BaseModel):
    response: Optional[Response] = None
    error_code: Union[int, str] = 0
    error_msg: str = 'unknown error'

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
        return BaseVkError(
            error_msg = error
        )

    class Config:
        arbitrary_types_allowed = True

