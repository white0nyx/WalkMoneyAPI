from pydantic import Field, EmailStr

from src.common.schemas import BaseSchema


class LoginSuccessSchema(BaseSchema):
    message: str = Field(default="Login successful")
    role: str = Field(default="User")

    @classmethod
    def model_validate(cls, obj, **kwargs):
        obj_dict = obj.__dict__.copy()
        obj_dict["role"] = obj.role.name
        return super().model_validate(obj_dict)


class LogoutSuccessSchema(BaseSchema):
    message: str = Field(default="Logout successful")


class LoginUserSchema(BaseSchema):
    email: EmailStr
    password: str


class ChangePasswordSchema(BaseSchema):
    email: EmailStr


class SetNewPasswordSchema(BaseSchema):
    reset_password_token: str
    password: str


class CreateUserSchema(BaseSchema):
    name: str
    email: EmailStr
    password: str
