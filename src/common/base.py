from sqlalchemy import MetaData
from sqlalchemy.orm import declared_attr, as_declarative

metadata = MetaData()


@as_declarative(metadata=metadata)
class Base:
    @classmethod
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    __allow_unmapped__ = False
