from enum import Enum

class DeactivatedEnum(str, Enum):
    deleted = 'deleted'
    banned = 'banned'
