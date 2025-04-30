from typing import Any
from typing import Optional

from mailtrap.mail.base_entity import BaseEntity


class Address(BaseEntity):
    def __init__(self, email: str, name: Optional[str] = None) -> None:
        self.email = email
        self.name = name

    @property
    def api_data(self) -> dict[str, Any]:
        return self.omit_none_values({"email": self.email, "name": self.name})
