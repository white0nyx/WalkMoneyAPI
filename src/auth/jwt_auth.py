import bcrypt

from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
from fastapi import HTTPException, Security, Depends
from fastapi.security import APIKeyCookie
from passlib.context import CryptContext

from src.user.models import User
from src.auth.repository import AuthRepository
from src.common.configuration import conf
from src.common.exceptions import (
    UserNotAuthorizedException,
    InvalidTokenException,
    UserAlreadyExistsException,
    UserNotActiveException,
    UserNotAdminException,
)

auth_scheme = APIKeyCookie(name="authorization", auto_error=False)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str, encoding: str = conf.token.default_encoding) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(encoding), salt).decode(encoding)


def verify_password(password: str, hashed_password: str, encoding: str = conf.token.default_encoding) -> bool:
    if bcrypt.checkpw(password.encode(encoding), hashed_password.encode(encoding)):
        return True
    return False


async def create_user(user_data: dict) -> User:
    try:
        auth_repository = AuthRepository()
        user = await auth_repository.find_by_email(user_data["email"])
        if user is not None:
            raise UserAlreadyExistsException
        user_data["password"] = get_password_hash(user_data["password"])
        user_data["role_id"] = await auth_repository.get_default_role_id()
        user = await auth_repository.add_one(user_data)
        return user
    except UserAlreadyExistsException:
        raise
    except Exception:
        raise


def create_access_token(email: str) -> str:
    data: dict[str, str | datetime] = {"sub": email}
    expires_delta = timedelta(minutes=conf.token.access_token_expire_minutes)
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, conf.token.secret_key, algorithm=conf.token.jwt_sign_algorithm)
    return encoded_jwt


async def get_user_from_db(email: str) -> User | None:
    try:
        auth_repository = AuthRepository()
        user = await auth_repository.find_by_email(email)
        return user
    except Exception:
        raise HTTPException(status_code=400, detail="Database connection error")


async def get_current_user(token_in_cookie: str = Security(auth_scheme)) -> User:
    try:
        if not token_in_cookie:
            raise UserNotAuthorizedException
        payload = jwt.decode(token_in_cookie, conf.token.secret_key, algorithms=[conf.token.jwt_sign_algorithm])
        email: str = payload.get("sub")
        exp_time = datetime.fromtimestamp(payload.get("exp"), tz=UTC)
        if email is None or (exp_time < datetime.now(UTC)):
            raise JWTError
        user = await get_user_from_db(email)
        if user is None:
            raise InvalidTokenException
        if not user.is_active:
            raise UserNotActiveException
        return user
    except UserNotAuthorizedException:
        raise
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except InvalidTokenException:
        raise
    except UserNotActiveException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Error getting authorization data")


async def get_admin_user(user: User = Depends(get_current_user)) -> User:
    try:
        if not user.is_admin:
            raise UserNotAdminException
        return user
    except UserNotAdminException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Error getting admin authorization data")


def get_current_user_with_roles(required_roles: list[str]):
    async def dependency(user: User = Depends(get_current_user)):
        if user.role.name in required_roles:
            return user
        else:
            raise HTTPException(status_code=403, detail="Permission denied")

    return dependency
