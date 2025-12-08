from typing import Optional
from fastapi import HTTPException, status


class ApplicationException(HTTPException):
    def __init__(self, status_code: int, detail: Optional[str] = None):
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(ApplicationException):
    def __init__(self, detail: Optional[str] = "Resource not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class PermissionDeniedException(ApplicationException):
    def __init__(self, detail: Optional[str] = "You don't have permission"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class BadRequestException(ApplicationException):
    def __init__(self, detail: Optional[str] = "Bad request"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class UnauthorizedException(ApplicationException):
    def __init__(self, detail: Optional[str] = "Unauthorized"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)
