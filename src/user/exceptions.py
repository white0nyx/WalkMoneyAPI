from fastapi import HTTPException

class UserNotFoundException(HTTPException):
    def __init__(self, status_code: int = 404, detail: str = "User not found"):
        super().__init__(status_code=status_code, detail=detail)