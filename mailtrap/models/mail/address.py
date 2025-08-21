from typing import Optional

from pydantic.dataclasses import dataclass

from mailtrap.models.common import ParametersObject


@dataclass
class Address(ParametersObject):
    email: str
    name: Optional[str] = None
