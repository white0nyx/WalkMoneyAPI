from src.category.main.exceptions import CategoryNotFoundException, CategoryPermissionDeniedException
from src.category.main.repository import CategoryRepository
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
            raise CategoryNotFoundException
        if category.user_id != user.id:
            raise CategoryPermissionDeniedException
        subcategory = await self.subcategory_repository.add_one(data.model_dump())
        return subcategory