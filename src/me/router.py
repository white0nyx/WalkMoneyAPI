import logging
from typing import Annotated

from fastapi import Depends, HTTPException, APIRouter

from src.auth import jwt_auth
from src.me.dependencies import me_service
from src.me.service import MeService
from src.user.models import User

router = APIRouter(
    prefix="",
    tags=["me_api"],
    responses={404: {"description": "Page not found"}},
)


@router.get("/me")
async def get_me(
    service: Annotated[MeService, Depends(me_service)],
    current_user: Annotated[User, Depends(jwt_auth.get_current_user)],
):
    try:
        me = await service.get_me(current_user.id)
        return me
    except Exception as e:
        logging.exception(f"Error getting a me data. Error: {e}")
        raise HTTPException(status_code=400, detail="Error getting a me data")
