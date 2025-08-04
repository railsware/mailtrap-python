from typing import Optional

from mailtrap import MailtrapClient
from mailtrap.schemas.projects import Project

API_TOKEN = "YOU_API_TOKEN"
ACCOUNT_ID = "YOU_ACCOUNT_ID"


def find_project_by_name(project_name: str, projects: list[Project]) -> Optional[str]:
    filtered_projects = [project for project in projects if project.name == project_name]
    if filtered_projects:
        return filtered_projects[0].id
    return None


MailtrapClient.configure_access_token(API_TOKEN)
testing_api = MailtrapClient.get_testing_api(ACCOUNT_ID)
projects_api = testing_api.projects

project_name = "Example-project"

created_project = projects_api.create(project_name=project_name)
projects = projects_api.get_list()
project_id = find_project_by_name(project_name, projects)
project = projects_api.get_by_id(project_id)
updated_project = projects_api.update(project_id, "Updated-project-name")
deleted_object = projects_api.delete(project_id)
