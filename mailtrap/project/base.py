from abc import ABCMeta
from collections.abc import Sequence
from typing import Any
from typing import Optional

from mailtrap.project.name import Name
from mailtrap.mail.base_entity import BaseEntity


class BaseProject(BaseEntity, metaclass=ABCMeta):
    """Base abstract class for projects."""

    def __init__(
        self,
        project: Optional[Name] = None

    ) -> None:
        self.project = project

    @property
    def api_data(self) -> dict[str, Any]:
        data: dict[str, Any] = {}

        if self.project is not None:
            data["project"] = self.project.api_data

        return self.omit_none_values(data)
