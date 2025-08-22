from typing import Optional

from pydantic.dataclasses import dataclass

from mailtrap.models.common import RequestParams


@dataclass
class CreateContactFieldParams(RequestParams):
    name: str
    data_type: str
    merge_tag: str


@dataclass
class UpdateContactFieldParams(RequestParams):
    name: Optional[str] = None
    merge_tag: Optional[str] = None

    def __post_init__(self) -> None:
        if all(value is None for value in [self.name, self.merge_tag]):
            raise ValueError("At least one field must be provided for update action")


@dataclass
class ContactField:
    id: int
    name: str
    data_type: str
    merge_tag: str
