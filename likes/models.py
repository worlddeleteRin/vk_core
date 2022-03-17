from typing import Any
from pydantic.main import BaseModel

from vk_core.models import BaseModelParseException


class IsLikedResponse(BaseModel):
    liked: int
    copied: int

    @staticmethod
    def process_from_response(resp: Any):
        parse_exception = BaseModelParseException(
            'IsLikedResponse parse error'
        )
        if not isinstance(resp, dict):
            raise parse_exception
        return IsLikedResponse(
            **resp
        )

    def isLiked(self):
        return self.liked == 1
    def isReplied(self):
        return self.copied == 1

