from typing import Any
from typing import Optional

from mailtrap.project.base import BaseProject
from mailtrap.project.name import Name


class Project(BaseProject):
    """Creates a request body for /api/accounts/{account_id}/projects Mailtrap API v2 endpoint.
    """

    def __init__(
        self,
        project: Optional[Name] = None
    ) -> None:
        super().__init__(
            project=project,
        )

    @property
    def api_data(self) -> dict[str, Any]:
        return self.omit_none_values(
            {
                **super().api_data,
            }
        )
