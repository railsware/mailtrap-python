from mailtrap.http import HttpClient
from mailtrap.models.base import DeletedObject
from mailtrap.models.projects import Project


class ProjectsApi:
    def __init__(self, account_id: str, client: HttpClient) -> None:
        self.account_id = account_id
        self.client = client

    def get_list(self) -> list[Project]:
        response = self.client.list(f"/api/accounts/{self.account_id}/projects")
        return [Project.from_dict(project) for project in response]

    def get_by_id(self, project_id: str) -> Project:
        response = self.client.get(f"/api/accounts/{self.account_id}/projects/{project_id}")
        return Project.from_dict(response)

    def create(self, project_name: str) -> Project:
        response = self.client.post(
            f"/api/accounts/{self.account_id}/projects",
            json={"project": {"name": project_name}},
        )
        return Project.from_dict(response)

    def update(self, project_id: str, project_name: str) -> Project:
        response = self.client.patch(
            f"/api/accounts/{self.account_id}/projects/{project_id}",
            json={"project": {"name": project_name}},
        )
        return Project.from_dict(response)

    def delete(self, project_id: str) -> DeletedObject:
        response = self.client.delete(
            f"/api/accounts/{self.account_id}/projects/{project_id}",
        )
        return DeletedObject(response["id"])
