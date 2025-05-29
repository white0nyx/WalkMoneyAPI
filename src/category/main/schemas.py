from src.common.schemas import BaseSchema


class GetCategoryBaseSchema(BaseSchema):
    id: int
    name: str
    icon_url: str | None = None


class CreateCategorySchema(BaseSchema):
    name: str
    icon_url: str | None = None


class UpdateCategorySchema(CreateCategorySchema):
    pass
