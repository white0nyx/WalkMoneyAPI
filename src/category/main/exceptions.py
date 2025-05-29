from fastapi import HTTPException


class CategoryNotFoundException(HTTPException):

    def __init__(self, status_code: int = 404, detail: str = "Category not found"):
        super().__init__(status_code=status_code, detail=detail)


class CategoryPermissionDeniedException(HTTPException):

    def __init__(self, status_code: int = 403, detail: str = "Permission denied for this category"):
        super().__init__(status_code=status_code, detail=detail)