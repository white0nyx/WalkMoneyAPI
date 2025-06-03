


import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from src.auth import jwt_auth
from src.subcategory.main.dependencies import subcategory_service
from src.subcategory.main.schemas import CreateSubCategorySchema, GetSubCategorySchema, ResponseGetSubCategorySchema, UpdateSubCategorySchema
from src.subcategory.main.service import SubCategoryService
from src.user.models import User

router = APIRouter(
    prefix="/subcategory",
    tags=["subcategory_api"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=GetSubCategorySchema)
async def create_subcategory(
    data: CreateSubCategorySchema,
    service: Annotated[SubCategoryService, Depends(subcategory_service)],
    user: User = Depends(jwt_auth.get_current_user),
):
    try:
        subcategory = await service.create_subcategory(data, user)
        return subcategory
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error creating subcategory. Error: {e}")
        raise HTTPException(status_code=400, detail="Error creating subcategory")

@router.get("", response_model=ResponseGetSubCategorySchema)
async def get_subcategories(
    category_id: int,
    service: Annotated[SubCategoryService, Depends(subcategory_service)],
    user: Annotated[User, Depends(jwt_auth.get_current_user),],
):
    try:
        subcategories = await service.get_subcategories(category_id, user.id)
        return subcategories
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error getting subcategories. Error: {e}")
        raise HTTPException(status_code=400, detail="Error getting subcategories")


@router.get("/{subcategory_id}", response_model=GetSubCategorySchema)
async def get_subcategory(
    subcategory_id: int,
    service: Annotated[SubCategoryService, Depends(subcategory_service)],
    user: Annotated[User, Depends(jwt_auth.get_current_user),],
):
    try:
        subcategory = await service.get_subcategory(subcategory_id, user.id)
        return subcategory
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error getting subcategory. Error: {e}")
        raise HTTPException(status_code=400, detail="Error getting subcategory")


@router.put("/{subcategory_id}", response_model=GetSubCategorySchema)
async def update_subcategory(
    subcategory_id: int,
    data: UpdateSubCategorySchema,
    service: Annotated[SubCategoryService, Depends(subcategory_service)],
    user: Annotated[User, Depends(jwt_auth.get_current_user),],
):
    try:
        subcategory = await service.update_subcategory(subcategory_id, data, user.id)
        return subcategory
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error updating subcategory. Error: {e}")
        raise HTTPException(status_code=400, detail="Error updating subcategory"
)

@router.delete("/{subcategory_id}")
async def delete_subcategory(
    subcategory_id: int,
    service: Annotated[SubCategoryService, Depends(subcategory_service)],
    user: Annotated[User, Depends(jwt_auth.get_current_user),],
):
    try:
        await service.delete_subcategory(subcategory_id, user.id)
        return {"message": "Subcategory deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logging.exception(f"Error deleting subcategory. Error: {e}")
        raise HTTPException(status_code=400, detail="Error deleting subcategory")
