from pydantic import BaseModel
from typing import Optional

class CategoryBaseSchema(BaseModel):
    name: str
    icon_url: Optional[str] = None
    is_archived: Optional[bool] = False

    class Config:
        orm_mode = True

class CreateCategorySchema(CategoryBaseSchema):
    pass

class UpdateCategorySchema(CategoryBaseSchema):
    pass

class CategorySchema(CategoryBaseSchema):
    id: int

    class Config:
        orm_mode = True
