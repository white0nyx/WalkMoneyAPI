import logging
from typing import List, Annotated

from fastapi import APIRouter, HTTPException, Depends

from src.auth import jwt_auth
from src.category.main.dependencies import get_category_service
from src.category.main.schemas import CreateCategorySchema, UpdateCategorySchema, GetCategoryBaseSchema, GetCategoryParamsSchema
from src.category.main.service import CategoryService
from src.user.models import User

router = APIRouter(
    prefix="/category_api",
    tags=["category_api"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=GetCategoryBaseSchema)
async def create_category(
    data: CreateCategorySchema,
    service: Annotated[CategoryService, Depends(get_category_service)],
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        category = await service.create_category(data, user)
        return category
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error creating category. Error: {e}")
        raise HTTPException(status_code=400, detail="Error creating category")


@router.get("/{category_id}", response_model=GetCategoryBaseSchema)
async def get_category(
    category_id: int,
    service: Annotated[CategoryService, Depends(get_category_service)],
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        category = await service.get_category(category_id, user)
        return category
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error getting category. Error: {e}")
        raise HTTPException(status_code=400, detail="Error getting category")


@router.get("", response_model=List[GetCategoryBaseSchema])
async def get_all_categories(
    params: Annotated[GetCategoryParamsSchema, Depends()],
    service: Annotated[CategoryService, Depends(get_category_service)],
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        categories = await service.get_all_categories(user.id, params)
        return categories
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error getting categories. Error: {e}")
        raise HTTPException(status_code=400, detail="Error getting categories")


@router.put("/{category_id}", response_model=GetCategoryBaseSchema)
async def update_category(
    category_id: int,
    category_data: UpdateCategorySchema,
    service: Annotated[CategoryService, Depends(get_category_service)],
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        category = await service.update_category(category_id, category_data, user)
        return category
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error updating categories. Error: {e}")
        raise HTTPException(status_code=400, detail="Error updating categories")


@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    category_service: CategoryService = Depends(get_category_service),
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        await category_service.delete_category(category_id, user)
        return {"message": "Category deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Category deletion error. Error: {e}")
        raise HTTPException(status_code=400, detail="Category deletion error")

