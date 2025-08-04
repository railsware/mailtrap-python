import logging
from typing import Optional

from mailtrap import MailtrapClient
from mailtrap.schemas.projects import Project

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

API_TOKEN = "YOU_API_TOKEN"
ACCOUNT_ID = "YOU_ACCOUNT_ID"


def find_project_by_name(project_name: str, projects: list[Project]) -> Optional[str]:
    filtered_projects = [project for project in projects if project.name == project_name]
    if filtered_projects:
        return filtered_projects[0].id
    return None


logging.info("Starting Mailtrap Testing API example...")

client = MailtrapClient(token=API_TOKEN)
testing_api = client.get_testing_api(ACCOUNT_ID)
projects_api = testing_api.projects

project_name = "Example-project"
created_project = projects_api.create(project_name=project_name)
logging.info(f"Project created! ID: {created_project.id}, Name: {created_project.name}")

projects = projects_api.get_list()
logging.info(f"Found {len(projects)} projects:")
for project in projects:
    logging.info(f"   - {project.name} (ID: {project.id})")

project_id = find_project_by_name(project_name, projects)
if project_id:
    logging.info(f"Found project with ID: {project_id}")
else:
    logging.info("Project not found in the list")

if project_id:
    project = projects_api.get_by_id(project_id)
    logging.info(f"Project details: {project.name} (ID: {project.id})")

    new_name = "Updated-project-name"
    updated_project = projects_api.update(project_id, new_name)
    logging.info(f"Project updated!ID: {project_id}, New name: {updated_project.name}")

    deleted_object = projects_api.delete(project_id)
    logging.info(f"Project deleted! Deleted ID: {deleted_object.id}")

logging.info("Example completed successfully!")
