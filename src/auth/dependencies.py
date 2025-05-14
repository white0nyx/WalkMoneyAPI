from src.auth.repository import AuthRepository
from src.auth.service import AuthService


def user_auth_service():
    return AuthService(AuthRepository)
