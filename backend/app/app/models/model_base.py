from typing import Any

from sqlalchemy import inspect
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import registry
from sqlalchemy.sql.schema import MetaData
from sqlalchemy_utils import JSONType

try:
    # Use JSONB
    from sqlalchemy.dialects.postgresql import JSONB

    postgres_jsonb = True
except Exception:
    postgres_jsonb = False


class JSONBType(JSONType):
    def load_dialect_impl(self, dialect: DefaultDialect) -> Any:
        if dialect.name == "postgresql" and postgres_jsonb:
            return dialect.type_descriptor(JSONB())
        return super(JSONBType, self).load_dialect_impl(dialect)


metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


def _filtered_constructor(self, **kwargs):
    """Custom constructor for all models that only grabs the items
    in kwargs that match the respective model's fields.
    """
    cls_ = type(self)
    for item in kwargs:
        if not hasattr(cls_, item):
            continue
        setattr(self, item, kwargs[item])


mapper_registry = registry(metadata=metadata, constructor=_filtered_constructor)


@mapper_registry.as_declarative_base()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def as_dict(self) -> dict:
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}
