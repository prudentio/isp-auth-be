from sqlalchemy.ext.declarative import as_declarative, declared_attr
import re

def to_snake_case(name: str) -> str:
    name = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
    name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
    return name.lower()

@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return to_snake_case(cls.__name__)
