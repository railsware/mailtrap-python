from typing import Any
from typing import Optional

from mailtrap.mail.base_entity import BaseEntity


class Name(BaseEntity):
    def __init__(self, name: Optional[str] = None) -> None:
        self.name = name

    @property
    def api_data(self) -> dict[str, Any]:
        return self.omit_none_values({"name": self.name})
