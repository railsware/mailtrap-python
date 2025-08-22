from typing import Optional

from pydantic.dataclasses import dataclass

from mailtrap.models.common import RequestParams


@dataclass
class Address(RequestParams):
    email: str
    name: Optional[str] = None
