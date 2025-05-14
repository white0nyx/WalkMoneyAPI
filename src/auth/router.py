import logging

from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, Request, Response

from src.auth import jwt_auth
from src.common.exceptions import UserAlreadyExistsException, UserCredentialsException, UserNotActiveException
from src.auth.schemas import *
from src.auth.service import AuthService
from src.auth.dependencies import user_auth_service

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Page not found"}},
)


@router.post("/register", response_model=LoginSuccessSchema)
async def create_user(
    request: Request,
    user_data: CreateUserSchema,
    auth_service: Annotated[AuthService, Depends(user_auth_service)],
):
    try:
        access_token = await auth_service.register_user(user_data, request)
        return access_token
    except UserAlreadyExistsException:
        raise
    except Exception as e:
        logging.exception(f"User registration error. Email: {user_data.email} Error: {e}")
        raise HTTPException(status_code=400, detail="User registration error")


@router.post("/login", response_model=LoginSuccessSchema)
async def login_for_token(
    request: Request,
    user_data: LoginUserSchema,
    auth_service: Annotated[AuthService, Depends(user_auth_service)],
):
    try:
        access_token = await auth_service.authenticate_user(user_data, request)
        return access_token
    except (UserCredentialsException, UserNotActiveException):
        raise
    except Exception as e:
        logging.exception(f"Error user auth (error create token). Username: {user_data.email} Error: {e}")
        raise HTTPException(status_code=400, detail="User authorization error")


@router.post(
    "/logout",
    response_model=LogoutSuccessSchema,
    dependencies=[Depends(jwt_auth.get_current_user)],
)
async def logout(response: Response, auth_service: Annotated[AuthService, Depends(user_auth_service)]):
    try:
        await auth_service.logout(response)
        return {"message": "Logout successful"}
    except Exception as e:
        logging.exception(f"Logout error. Error: {e}")
        raise HTTPException(status_code=400, detail="Logout error")


@router.post("/forgot_password")
async def forgot_password(user_data: ChangePasswordSchema, auth_service: Annotated[AuthService, Depends(user_auth_service)]):
    try:
        await auth_service.restore_password(user_data)
        return {"message": "Check your email address"}
    except Exception as e:
        logging.exception(f"Error user password recovery. Email: {user_data.email}. Error: {e}")
        raise HTTPException(status_code=400, detail="Error user password recovery.")


@router.post("/restore_password")
async def restore_password(user_data: SetNewPasswordSchema, auth_service: Annotated[AuthService, Depends(user_auth_service)]):
    try:
        await auth_service.set_new_password(user_data)
        return {"message": "Password changed successfully"}
    except Exception as e:
        logging.exception(f"Error changing user password. Error: {e}")
        raise HTTPException(status_code=400, detail="Error changing user password.")
