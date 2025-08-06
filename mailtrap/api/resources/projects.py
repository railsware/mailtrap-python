from mailtrap.http import HttpClient
from mailtrap.models.common import DeletedObject
from mailtrap.models.projects import Project


class ProjectsApi:
    def __init__(self, client: HttpClient, account_id: str) -> None:
        self.account_id = account_id
        self.client = client

    def get_list(self) -> list[Project]:
        response = self.client.get(f"/api/accounts/{self.account_id}/projects")
        return [Project(**project) for project in response]

    def get_by_id(self, project_id: int) -> Project:
        response = self.client.get(
            f"/api/accounts/{self.account_id}/projects/{project_id}"
        )
        return Project(**response)

    def create(self, project_name: str) -> Project:
        response = self.client.post(
            f"/api/accounts/{self.account_id}/projects",
            json={"project": {"name": project_name}},
        )
        return Project(**response)

    def update(self, project_id: int, project_name: str) -> Project:
        response = self.client.patch(
            f"/api/accounts/{self.account_id}/projects/{project_id}",
            json={"project": {"name": project_name}},
        )
        return Project(**response)

    def delete(self, project_id: int) -> DeletedObject:
        response = self.client.delete(
            f"/api/accounts/{self.account_id}/projects/{project_id}",
        )
        return DeletedObject(**response)
