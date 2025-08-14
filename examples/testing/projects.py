from mailtrap import MailtrapClient
from mailtrap.models.projects import Project

API_TOKEN = "YOU_API_TOKEN"
ACCOUNT_ID = "YOU_ACCOUNT_ID"

client = MailtrapClient(token=API_TOKEN, account_id=ACCOUNT_ID)
projects_api = client.testing_api.projects


def list_projects() -> list[Project]:
    return projects_api.get_list()


def create_project(project_name: str) -> Project:
    return projects_api.create(project_name=project_name)


def update_project(project_id: str, new_name: str) -> Project:
    return projects_api.update(project_id, new_name)


def delete_project(project_id: str):
    return projects_api.delete(project_id)


if __name__ == "__main__":
    projects = list_projects()
    print(projects)
