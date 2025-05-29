from src.common.schemas import BaseSchema

class GetSubCategoryBaseSchema(BaseSchema):
    id: int
    name: str
    icon_url: str | None = None
    category_id: int

class CreateSubCategorySchema(BaseSchema):
    name: str
    icon_url: str | None = None
    category_id: int

class UpdateSubCategorySchema(CreateSubCategorySchema):
    pass