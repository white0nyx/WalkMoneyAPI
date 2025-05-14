from fastapi import HTTPException


class UserNotAuthorizedException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="User is not authorized")


class UserCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Incorrect username or password")


class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail="User with this email already exists")


class InvalidTokenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid token")


class UserNotActiveException(HTTPException):
    def __init__(self):
        super().__init__(status_code=403, detail="Account is not active")


class UserNotAdminException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=403,
            detail="Permission denied. User not admin",
        )


class TaskNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=404,
            detail="Task not found",
        )


class WrongFileFormatException(HTTPException):
    def __init__(self, message="Wrong file format"):
        super().__init__(status_code=415, detail=message)


class FileSizeExceededException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=413,
            detail="Maximum allowed file size exceeded",
        )


class WrongImageFormat(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=406,
            detail="Wrong image format. Allowed: jpeg, jpg, png, webp",
        )
