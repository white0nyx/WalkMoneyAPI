from fastapi import HTTPException


class AccountNotFoundException(HTTPException):

    def __init__(self, status_code: int = 404, detail: str = "Account not found"):
        super().__init__(status_code=status_code, detail=detail)


class AccountPermissionDeniedException(HTTPException):

    def __init__(self, status_code: int = 403, detail: str = "Account denied for this category"):
        super().__init__(status_code=status_code, detail=detail)