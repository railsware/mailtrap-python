from dataclasses import dataclass, fields, is_dataclass
from typing import Any, Type, TypeVar, get_args, get_origin


T = TypeVar("T", bound="BaseModel")


@dataclass
class BaseModel:
    @classmethod
    def from_dict(cls: Type[T], data: dict[str, Any]) -> T:
        values: dict[str, Any] = {}
        for field in fields(cls):
            value = data.get(field.name)

            if value is None:
                values[field.name] = None
                continue

            field_type = field.type
            values[field.name] = cls._parse_value(value, field_type)

        return cls(**values)

    @classmethod
    def _parse_value(cls, value: Any, field_type: Any) -> Any:
        origin = get_origin(field_type)

        if origin is list:
            item_type = get_args(field_type)[0]
            return [cls._parse_value(item, item_type) for item in value]

        if is_dataclass(field_type) and hasattr(field_type, "from_dict"):
            return field_type.from_dict(value)

        return value



@dataclass
class DeletedObject(BaseModel):
    id: str
