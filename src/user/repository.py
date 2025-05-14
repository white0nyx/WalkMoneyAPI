from src.common.repository import SQLAlchemyRepository
from src.user.models import User


class UserRepository(SQLAlchemyRepository):
    model: type[User] = User