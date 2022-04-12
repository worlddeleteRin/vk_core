class GroupNotFoundException(Exception):
    def __init__(
        self, 
        message: str = 'group not found'
    ):
        super().__init__(message)
