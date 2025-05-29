


import logging
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends

from src.auth import jwt_auth
from src.subcategory.main.dependencies import subcategory_service
from src.subcategory.main.schemas import CreateSubCategorySchema, GetSubCategoryBaseSchema
from src.subcategory.main.service import SubCategoryService
from src.user.models import User

router = APIRouter(
    prefix="/subcategory_api",
    tags=["subcategory_api"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=GetSubCategoryBaseSchema)
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


@router.get("/{subcategory_id}", response_model=GetSubCategoryBaseSchema)
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
