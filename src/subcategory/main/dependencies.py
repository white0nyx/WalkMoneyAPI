from src.category.main.repository import CategoryRepository
from src.subcategory.main.repository import SubCategoryRepository
from src.subcategory.main.service import SubCategoryService


def subcategory_service() -> SubCategoryService:
    return SubCategoryService(SubCategoryRepository(), CategoryRepository())