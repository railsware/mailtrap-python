from typing import Any

import pytest
import responses

from mailtrap.api.resources.projects import ProjectsApi
from mailtrap.config import MAILTRAP_HOST
from mailtrap.exceptions import APIError
from mailtrap.http import HttpClient
from mailtrap.schemas.base import DeletedObject
from mailtrap.schemas.projects import Project

ACCOUNT_ID = "321"
PROJECT_ID = 123
BASE_PROJECTS_URL = f"https://{MAILTRAP_HOST}/api/accounts/{ACCOUNT_ID}/projects"


@pytest.fixture
def client() -> ProjectsApi:
    return ProjectsApi(account_id=ACCOUNT_ID, client=HttpClient(MAILTRAP_HOST))


@pytest.fixture
def sample_project_dict() -> dict[str, Any]:
    return {
        "id": PROJECT_ID,
        "name": "Test Project",
        "inboxes": [],
        "share_links": {
            "admin": "https://mailtrap.io/projects/321/admin",
            "viewer": "https://mailtrap.io/projects/321/viewer",
        },
        "permissions": {
            "can_read": True,
            "can_update": True,
            "can_destroy": True,
            "can_leave": True,
        },
    }


class TestProjectsApi:
    @responses.activate
    def test_get_list_should_return_project_list(
        self, client: ProjectsApi, sample_project_dict: dict
    ) -> None:
        responses.add(
            responses.GET,
            BASE_PROJECTS_URL,
            json=[sample_project_dict],
            status=200,
        )

        projects = client.get_list()

        assert isinstance(projects, list)
        assert all(isinstance(p, Project) for p in projects)
        assert projects[0].id == PROJECT_ID

    @responses.activate
    def test_get_by_id_should_raise_not_found_error(self, client: ProjectsApi) -> None:
        url = f"{BASE_PROJECTS_URL}/{PROJECT_ID}"
        responses.add(
            responses.GET,
            url,
            status=404,
            json={"error": "Not Found"},
        )

        with pytest.raises(APIError) as exc_info:
            client.get_by_id(PROJECT_ID)

        assert "Not Found" in str(exc_info)

    @responses.activate
    def test_get_by_id_should_return_single_project(
        self, client: ProjectsApi, sample_project_dict: dict
    ) -> None:
        url = f"{BASE_PROJECTS_URL}/{PROJECT_ID}"
        responses.add(
            responses.GET,
            url,
            json=sample_project_dict,
            status=200,
        )

        project = client.get_by_id(PROJECT_ID)

        assert isinstance(project, Project)
        assert project.id == PROJECT_ID

    @responses.activate
    def test_create_should_return_new_project(
        self, client: ProjectsApi, sample_project_dict: dict
    ) -> None:
        responses.add(
            responses.POST,
            BASE_PROJECTS_URL,
            json=sample_project_dict,
            status=201,
        )

        project = client.create(project_name="New Project")

        assert isinstance(project, Project)
        assert project.name == "Test Project"

    @responses.activate
    def test_update_should_raise_not_found_error(self, client: ProjectsApi) -> None:
        url = f"{BASE_PROJECTS_URL}/{PROJECT_ID}"
        responses.add(
            responses.PATCH,
            url,
            status=404,
            json={"error": "Not Found"},
        )

        with pytest.raises(APIError) as exc_info:
            client.update(PROJECT_ID, project_name="Update Project Name")

        assert "Not Found" in str(exc_info)

    @responses.activate
    def test_update_should_return_updated_project(
        self, client: ProjectsApi, sample_project_dict: dict
    ) -> None:
        url = f"{BASE_PROJECTS_URL}/{PROJECT_ID}"
        updated_name = "Updated Project"
        updated_project_dict = sample_project_dict.copy()
        updated_project_dict["name"] = updated_name

        responses.add(
            responses.PATCH,
            url,
            json=updated_project_dict,
            status=200,
        )

        project = client.update(PROJECT_ID, project_name=updated_name)

        assert isinstance(project, Project)
        assert project.name == updated_name

    @responses.activate
    def test_delete_should_raise_not_found_error(self, client: ProjectsApi) -> None:
        url = f"{BASE_PROJECTS_URL}/{PROJECT_ID}"
        responses.add(
            responses.DELETE,
            url,
            status=404,
            json={"error": "Not Found"},
        )

        with pytest.raises(APIError) as exc_info:
            client.delete(PROJECT_ID)

        assert "Not Found" in str(exc_info)

    @responses.activate
    def test_delete_should_return_deleted_object(self, client: ProjectsApi) -> None:
        url = f"{BASE_PROJECTS_URL}/{PROJECT_ID}"
        responses.add(
            responses.DELETE,
            url,
            json={"id": PROJECT_ID},
            status=200,
        )

        result = client.delete(PROJECT_ID)

        assert isinstance(result, DeletedObject)
        assert result.id == PROJECT_ID
