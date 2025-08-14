from pydantic.dataclasses import dataclass


@dataclass
class DeletedObject:
    id: int
