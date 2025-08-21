from typing import Optional

from pydantic.dataclasses import dataclass

from mailtrap.models.common import RequestModel


@dataclass
class Address(RequestModel):
    email: str
    name: Optional[str] = None
