from fastapi import Depends, HTTPException
from src.category.service import CategoryService
from src.category.repository import CategoryRepository
from src.user.models import User
from src.user.repository import UserRepository
from sqlalchemy.orm import Session
from typing import Type

def get_category_service(
    category_repository: CategoryRepository = Depends(),
) -> CategoryService:
    return CategoryService(category_repository)
