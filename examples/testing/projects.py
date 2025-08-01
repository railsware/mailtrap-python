import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from typing import Optional
from mailtrap import MailtrapClient
from mailtrap.models.projects import Project

API_TOKEN = "YOU_API_TOKEN"
ACCOUNT_ID = "YOU_ACCOUNT_ID"


def find_project_by_name(project_name: str, projects: list[Project]) -> Optional[str]:
    filtered_projects = [project for project in projects if project.name == project_name]
    if filtered_projects:
        return filtered_projects[0].id
    return None


client = MailtrapClient(token=API_TOKEN, account_id=ACCOUNT_ID)
api = client.testing.projects

project_name = "Example-project"

created_project = api.create(project_name=project_name)
projects = api.get_list()
project_id = find_project_by_name(project_name, projects)
project = api.get_by_id(project_id)
updated_projected = api.update(project_id, "Updated-project-name")
api.delete(project_id)
