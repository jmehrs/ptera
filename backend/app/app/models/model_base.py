from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.sql.schema import MetaData
from sqlalchemy.engine.default import DefaultDialect
from sqlalchemy_utils import JSONType

try:
    # Use JSONB
    from sqlalchemy.dialects.postgresql import JSONB

    postgres_jsonb = True
except:
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


@as_declarative(metadata=metadata)
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
