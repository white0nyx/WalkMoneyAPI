from src.common.repository import SQLAlchemyRepository
from src.subcategory.main.models import SubCategory


class SubCategoryRepository(SQLAlchemyRepository):
    model: type[SubCategory] = SubCategory