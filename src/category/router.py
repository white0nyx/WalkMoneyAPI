import logging
from typing import List

from fastapi import APIRouter, HTTPException, Depends

from src.auth import jwt_auth
from src.category.dependencies import get_category_service
from src.category.schemas import CategorySchema, CreateCategorySchema, UpdateCategorySchema
from src.category.service import CategoryService, CategoryNotFoundError, AccessForbiddenError
from src.user.models import User

router = APIRouter(
    prefix="/category_api",
    tags=["category_api"],
    responses={404: {"description": "Not found"}},
)

@router.post("/categories", response_model=CategorySchema)
async def create_category(
    category_data: CreateCategorySchema,
    category_service: CategoryService = Depends(get_category_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        category = await category_service.create_category(category_data.model_dump(), user)
        return category
    except Exception as e:
        logging.exception(f"Category creation error. Data: {category_data} Error: {e}")
        raise HTTPException(status_code=400, detail="Category creation error")


@router.get("/categories/{category_id}", response_model=CategorySchema)
async def get_category(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        category = await category_service.get_category(category_id, user)
        return category
    except CategoryNotFoundError:
        raise HTTPException(status_code=404, detail="Category not found")
    except AccessForbiddenError:
        raise HTTPException(status_code=403, detail="Access to this category is forbidden")


@router.get("/categories", response_model=List[CategorySchema])
async def get_all_categories(
    category_service: CategoryService = Depends(get_category_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        categories = await category_service.get_all_categories(user)
        return categories
    except AccessForbiddenError:
        raise HTTPException(status_code=403, detail="Access to categories is forbidden")


@router.put("/categories/{category_id}", response_model=CategorySchema)
async def update_category(
    category_id: int,
    category_data: UpdateCategorySchema,
    category_service: CategoryService = Depends(get_category_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        category = await category_service.update_category(category_id, category_data.model_dump(), user)
        return category
    except CategoryNotFoundError:
        raise HTTPException(status_code=404, detail="Category not found")
    except AccessForbiddenError:
        raise HTTPException(status_code=403, detail="Access to this category is forbidden")


@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        await category_service.delete_category(category_id, user)
        return "Category deleted"
    except CategoryNotFoundError:
        raise HTTPException(status_code=404, detail="Category not found")
    except AccessForbiddenError:
        raise HTTPException(status_code=403, detail="Access to this category is forbidden")


@router.get("/categories/active", response_model=List[CategorySchema])
async def get_active_categories(
    category_service: CategoryService = Depends(get_category_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        categories = await category_service.find_active_categories(user)
        return categories
    except AccessForbiddenError:
        raise HTTPException(status_code=403, detail="Access to categories is forbidden")
