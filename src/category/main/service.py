from src.category.main.exceptions import CategoryNotFoundException, CategoryPermissionDeniedException
from src.category.main.models import Category
from src.category.main.repository import CategoryRepository
from src.category.main.schemas import CreateCategorySchema, UpdateCategorySchema, GetCategoryParamsSchema
from src.user.models import User


class CategoryService:

    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    async def create_category(self, category_data: CreateCategorySchema, user: User) -> Category:
        category_data = category_data.model_dump()
        category_data["user_id"] = user.id
        category = await self.category_repository.add_one(category_data)
        return category

    async def get_category(self, category_id: int, user: User):
        category = await self.category_repository.find_one(category_id)
        if not category:
            raise CategoryNotFoundException
        if category.user_id != user.id:
            raise CategoryPermissionDeniedException
        return category

    async def get_all_categories(self, user_id: int, params: GetCategoryParamsSchema):
        categories = await self.category_repository.find_all_by_user_id(user_id, params)
        return categories

    async def update_category(self, category_id: int, category_data: UpdateCategorySchema, user: User):
        category = await self.category_repository.find_one(category_id)
        if not category:
            raise CategoryNotFoundException
        if category.user_id != user.id:
            raise CategoryPermissionDeniedException
        updated_category = await self.category_repository.update_one(category_id, category_data.model_dump())
        return updated_category

    async def delete_category(self, category_id: int, user: User):
        category = await self.category_repository.find_one(category_id)
        if not category:
            raise CategoryNotFoundException
        if category.user_id != user.id:
            raise CategoryPermissionDeniedException
        await self.category_repository.delete_one(category_id)
        return {"message": "Category deleted successfully"}

