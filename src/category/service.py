from src.category.repository import CategoryRepository
from src.category.models import Category
from src.user.models import User
from fastapi import HTTPException, status
from typing import List, Optional


class CategoryNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found.")


class AccessForbiddenError(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Access to this category is forbidden.")


class CategoryService:

    def __init__(self, category_repository: CategoryRepository):
        self.category_repository = category_repository

    async def create_category(self, data: dict, user: User) -> Category:
        if not self.has_access(user):
            raise AccessForbiddenError()
        return await self.category_repository.add_one(data)

    async def get_category(self, category_id: int, user: User) -> Optional[Category]:
        category = await self.category_repository.find_one(category_id)
        if not category:
            raise CategoryNotFoundError()
        if not self.has_access(user):
            raise AccessForbiddenError()
        return category

    async def get_all_categories(self, user: User) -> List[Category]:
        if not self.has_access(user):
            raise AccessForbiddenError()
        return await self.category_repository.find_all()

    async def update_category(self, category_id: int, data: dict, user: User) -> Optional[Category]:
        category = await self.category_repository.find_one(category_id)
        if not category:
            raise CategoryNotFoundError()
        if not self.has_access(user):
            raise AccessForbiddenError()
        return await self.category_repository.update_one(category_id, data)

    async def delete_category(self, category_id: int, user: User) -> None:
        category = await self.category_repository.find_one(category_id)
        if not category:
            raise CategoryNotFoundError()
        if not self.has_access(user):
            raise AccessForbiddenError()
        await self.category_repository.delete_one(category_id)

    async def find_category_by_name(self, name: str, user: User) -> Optional[Category]:
        if not self.has_access(user):
            raise AccessForbiddenError()
        return await self.category_repository.find_by_name(name)

    async def find_active_categories(self, user: User) -> List[Category]:
        if not self.has_access(user):
            raise AccessForbiddenError()
        return await self.category_repository.find_active_categories()

    def has_access(self, user: User) -> bool:
        # Логика проверки доступа пользователя к категориям.
        # Например, проверка, есть ли у пользователя роль администратора или нужные права.
        return user.role.name == "admin"  # Пример, можно изменить под вашу логику.
