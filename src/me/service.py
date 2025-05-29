from src.me.schemas import GetMeSchema
from src.user.exceptions import UserNotFoundException
from src.user.repository import UserRepository


class MeService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def get_me(self, user_id: int) -> GetMeSchema:
        user = await self.user_repository.find_one(user_id)
        if user is None:
            raise UserNotFoundException
        print(1)
        return GetMeSchema.model_validate(user)