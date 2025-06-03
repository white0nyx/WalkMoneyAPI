from fastapi import HTTPException


class TransactionNotFoundException(HTTPException):

    def __init__(self, status_code: int = 404, detail: str = "Transaction not found"):
        super().__init__(status_code=status_code, detail=detail)


class TransactionPermissionDeniedException(HTTPException):

    def __init__(self, status_code: int = 403, detail: str = "Permission denied for this transaction"):
        super().__init__(status_code=status_code, detail=detail)