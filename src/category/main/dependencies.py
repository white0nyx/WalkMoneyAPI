from fastapi import Depends
from src.category.main.service import CategoryService
from src.category.main.repository import CategoryRepository


def get_category_service(
    category_repository: CategoryRepository = Depends(),
) -> CategoryService:
    return CategoryService(category_repository)
