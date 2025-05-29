from src.me.service import MeService
from src.user.repository import UserRepository


def me_service() -> MeService:
    return MeService(UserRepository())