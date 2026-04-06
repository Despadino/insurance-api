from typing import Optional

from fastapi import HTTPException

from app.utils.errors.response_code import CustomErrorCode


class ErrorService:
    @staticmethod
    def error(
        method: CustomErrorCode,
        details: Optional[dict] = {},
    ) -> HTTPException:
        response_detail = {
            "code": method.code,
            "message": method.msg,
        }

        if details and len(details) > 0:
            response_detail["details"] = details
        
        return HTTPException(status_code=method.http_code, detail=response_detail)

error_service = ErrorService()