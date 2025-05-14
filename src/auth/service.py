from datetime import datetime, timedelta, UTC
from fastapi import Request, Response
from fastapi.responses import JSONResponse

from src.auth import jwt_auth
from src.common.repository import AbstractRepository
from src.common.exceptions import UserCredentialsException, UserNotActiveException
from src.common.smtp import send_password_reset_email
from src.auth.jwt_auth import get_password_hash
from src.auth.repository import AuthRepository
from src.auth.schemas import CreateUserSchema, LoginUserSchema, ChangePasswordSchema, SetNewPasswordSchema


class AuthService:
    def __init__(self, auth_repository: AbstractRepository.__class__):
        self.auth_repository: AuthRepository = auth_repository()

    async def register_user(self, user_data: CreateUserSchema, request: Request):
        await jwt_auth.create_user(user_data.model_dump())
        access_token = await self.authenticate_user(user_data, request)
        return access_token

    async def authenticate_user(self, user_data: LoginUserSchema | CreateUserSchema, request: Request):
        try:
            user = await self.auth_repository.find_by_email(user_data.email)
            if not user:
                raise UserCredentialsException
            check_pass = jwt_auth.verify_password(user_data.password, user.password)
            if not check_pass:
                raise UserCredentialsException
            if not user.is_active:
                raise UserNotActiveException
            access_token = jwt_auth.create_access_token(email=user.email)
            user_role = user.role.name
            response = JSONResponse({"message": "Login successful", "role": user_role})
            response.set_cookie(
                key="authorization",
                value=access_token,
                httponly=True,
                expires=datetime.now(UTC) + timedelta(minutes=jwt_auth.conf.token.access_token_expire_minutes),
                path="/",
                secure=False,  # Set it to True if you're using HTTPS
                samesite="lax",
            )
            client_ip = request.headers.get("X-Real-IP") if request.headers.get("X-Real-IP") else request.client.host
            await self.auth_repository.record_statistics(user.id, client_ip)
            return response
        except UserCredentialsException:
            raise
        except UserNotActiveException:
            raise
        except Exception:
            raise

    async def logout(self, response: Response):
        return response.delete_cookie("authorization")

    async def restore_password(self, user_data: ChangePasswordSchema):
        user = await self.auth_repository.create_password_reset_token(user_data.email)
        await send_password_reset_email(user)
        return

    async def set_new_password(self, user_data: SetNewPasswordSchema):
        user_data = user_data.model_dump()
        user_data["password"] = get_password_hash(user_data["password"])
        await self.auth_repository.set_new_password(user_data)
        return
