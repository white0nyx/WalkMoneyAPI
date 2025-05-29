from fastapi import HTTPException


class SubCategoryNotFoundException(HTTPException):

    def __init__(self, status_code: int = 404, detail: str = "SubCategory not found"):
        super().__init__(status_code=status_code, detail=detail)


class SubCategoryPermissionDeniedException(HTTPException):

    def __init__(self, status_code: int = 403, detail: str = "Permission denied for this subcategory"):
        super().__init__(status_code=status_code, detail=detail)