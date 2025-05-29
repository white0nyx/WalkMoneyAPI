from src.category.main.repository import CategoryRepository
from src.subcategory.main.exceptions import SubCategoryNotFoundException, SubCategoryPermissionDeniedException
from src.subcategory.main.repository import SubCategoryRepository
from src.subcategory.main.schemas import CreateSubCategorySchema
from src.user.models import User


class SubCategoryService:

    def __init__(
            self,
            subcategory_repository: SubCategoryRepository,
            category_repository: CategoryRepository,
    ):
        self.subcategory_repository = subcategory_repository
        self.category_repository = category_repository

    async def create_subcategory(self, data: CreateSubCategorySchema, user: User):
        category = await self.category_repository.find_one(data.category_id)
        if not category:
            raise SubCategoryNotFoundException
        if category.user_id != user.id:
            raise SubCategoryPermissionDeniedException
        subcategory = await self.subcategory_repository.add_one(data.model_dump())
        return subcategory

    async def get_subcategories(self, category_id: int, user_id: int):
        category = await self.category_repository.find_one(category_id)
        if not category:
            raise SubCategoryNotFoundException
        if category.user_id != user_id:
            raise SubCategoryPermissionDeniedException
        subcategories = await self.subcategory_repository.find_all_by_category_id(category_id)
        return {"subcategories": subcategories}

    async def get_subcategory(self, subcategory_id: int, user_id: int):
        subcategory = await self.subcategory_repository.find_one(subcategory_id)
        if not subcategory:
            raise SubCategoryNotFoundException
        if subcategory.category.user_id != user_id:
            raise SubCategoryPermissionDeniedException
        return subcategory

    async def update_subcategory(self, subcategory_id: int, data: CreateSubCategorySchema, user_id: int):
        subcategory = await self.subcategory_repository.find_one(subcategory_id)
        if not subcategory:
            raise SubCategoryNotFoundException
        if subcategory.category.user_id != user_id:
            raise SubCategoryPermissionDeniedException
        updated_subcategory = await self.subcategory_repository.update_one(subcategory_id, data.model_dump())
        return updated_subcategory

    async def delete_subcategory(self, subcategory_id: int, user_id: int) -> None:
        subcategory = await self.subcategory_repository.find_one(subcategory_id)
        if not subcategory:
            raise SubCategoryNotFoundException
        if subcategory.category.user_id != user_id:
            raise SubCategoryPermissionDeniedException
        await self.subcategory_repository.delete_one(subcategory_id)
