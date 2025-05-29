from src.common.schemas import BaseSchema

class GetSubCategorySchema(BaseSchema):
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


class ResponseGetSubCategorySchema(BaseSchema):
    subcategories: list[GetSubCategorySchema]
