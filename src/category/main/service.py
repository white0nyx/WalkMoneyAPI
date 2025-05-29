from src.category.main.repository import CategoryRepository
from src.category.main.schemas import CreateCategorySchema, UpdateCategorySchema
from src.user.models import User


class CategoryService:

    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    async def create_category(self, category_data: CreateCategorySchema, user: User):
        pass

    async def get_category(self, category_id: int, user: User):
        pass

    async def get_all_categories(self, user_id: int):
        categories = await self.category_repository.find_all_by_user_id(user_id)
        return categories

    async def update_category(self, category_id: int, category_data: UpdateCategorySchema, user: User):
        pass

    async def delete_category(self, category_id: int, user: User):
        pass

