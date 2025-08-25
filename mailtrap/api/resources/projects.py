from typing import Optional

from mailtrap.http import HttpClient
from mailtrap.models.common import DeletedObject
from mailtrap.models.projects import Project


class ProjectsApi:
    def __init__(self, client: HttpClient, account_id: str) -> None:
        self._account_id = account_id
        self._client = client

    def get_list(self) -> list[Project]:
        response = self._client.get(self._api_path())
        return [Project(**project) for project in response]

    def get_by_id(self, project_id: int) -> Project:
        response = self._client.get(self._api_path(project_id))
        return Project(**response)

    def create(self, project_name: str) -> Project:
        response = self._client.post(
            self._api_path(),
            json={"project": {"name": project_name}},
        )
        return Project(**response)

    def update(self, project_id: int, project_name: str) -> Project:
        response = self._client.patch(
            self._api_path(project_id),
            json={"project": {"name": project_name}},
        )
        return Project(**response)

    def delete(self, project_id: int) -> DeletedObject:
        response = self._client.delete(self._api_path(project_id))
        return DeletedObject(**response)

    def _api_path(self, project_id: Optional[int] = None) -> str:
        path = f"/api/accounts/{self._account_id}/projects"
        if project_id:
            return f"{path}/{project_id}"
        return path
