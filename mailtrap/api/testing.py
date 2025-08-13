from typing import Optional

from mailtrap.api.resources.projects import ProjectsApi
from mailtrap.http import HttpClient


class TestingApi:
    def __init__(
        self, client: HttpClient, account_id: str, inbox_id: Optional[str] = None
    ) -> None:
        self._account_id = account_id
        self._inbox_id = inbox_id
        self._client = client

    @property
    def projects(self) -> ProjectsApi:
        return ProjectsApi(account_id=self._account_id, client=self._client)
