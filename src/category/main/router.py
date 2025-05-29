import logging
from typing import List

from fastapi import APIRouter, HTTPException, Depends

from src.auth import jwt_auth
from src.category.main.dependencies import get_category_service
from src.category.main.schemas import CategorySchema, CreateCategorySchema, UpdateCategorySchema
from src.category.main.service import CategoryService
from src.user.models import User

router = APIRouter(
    prefix="/category_api",
    tags=["category_api"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=CategorySchema)
async def create_category(
    category_data: CreateCategorySchema,
    category_service: CategoryService = Depends(get_category_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        category = await category_service.create_category(category_data, user)
        return category
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Category creation error. Data: {category_data} Error: {e}")
        raise HTTPException(status_code=400, detail="Category creation error")


@router.get("/{category_id}", response_model=CategorySchema)
async def get_category(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        category = await category_service.get_category(category_id, user)
        return category
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error fetching category. Category ID: {category_id} Error: {e}")
        raise HTTPException(status_code=400, detail="Error fetching category")


@router.get("", response_model=List[CategorySchema])
async def get_all_categories(
    category_service: CategoryService = Depends(get_category_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        categories = await category_service.get_all_categories(user.id)
        return categories
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error fetching categories for user ID: {user.id} Error: {e}")
        raise HTTPException(status_code=400, detail="Error fetching categories")


@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(
    category_id: int,
    category_data: UpdateCategorySchema,
    category_service: CategoryService = Depends(get_category_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        category = await category_service.update_category(category_id, category_data.model_dump(), user)
        return category
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Category update error. Category ID: {category_id} Data: {category_data} Error: {e}")
        raise HTTPException(status_code=400, detail="Category update error")


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        await category_service.delete_category(category_id, user)
        return "Category deleted"
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Category deletion error. Category ID: {category_id} Error: {e}")
        raise HTTPException(status_code=400, detail="Category deletion error")

