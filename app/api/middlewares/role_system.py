from fastapi import Depends

from app.api.middlewares.current_user import get_current_user
from app.core.enum import UserRoleEnum
from app.models.user.schemas import UserRead
from app.utils.errors.error import CustomErrorCode, error_service


def roles_required(*required_roles: UserRoleEnum):
    async def check_roles(
        current_user: UserRead = Depends(get_current_user),
    ) -> UserRead:
        if not required_roles:
            return current_user

        if current_user.role not in required_roles:
            raise error_service.error(
                CustomErrorCode.HTTP_403_FORBIDDEN,
            )
        return current_user

    return check_roles
