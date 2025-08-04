from typing import Any

import pytest
import responses
from pydantic import ValidationError

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

    @pytest.mark.parametrize(
        "status_code,response_json,expected_error_message",
        [
            (401, {"error": "Incorrect API token"}, "Incorrect API token"),
            (403, {"errors": "Access forbidden"}, "Access forbidden"),
        ],
    )
    @responses.activate
    def test_get_list_should_raise_api_errors(
        self,
        client: ProjectsApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.add(
            responses.GET,
            BASE_PROJECTS_URL,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.get_list()

        assert expected_error_message in str(exc_info.value)

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

    @pytest.mark.parametrize(
        "status_code,response_json,expected_error_message",
        [
            (401, {"error": "Incorrect API token"}, "Incorrect API token"),
            (403, {"errors": "Access forbidden"}, "Access forbidden"),
            (404, {"error": "Not Found"}, "Not Found"),
        ],
    )
    @responses.activate
    def test_get_by_id_should_raise_api_errors(
        self,
        client: ProjectsApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        url = f"{BASE_PROJECTS_URL}/{PROJECT_ID}"
        responses.add(
            responses.GET,
            url,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.get_by_id(PROJECT_ID)

        assert expected_error_message in str(exc_info.value)

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

    @pytest.mark.parametrize(
        "status_code,response_json,expected_error_message",
        [
            (401, {"error": "Incorrect API token"}, "Incorrect API token"),
            (403, {"errors": "Access forbidden"}, "Access forbidden"),
        ],
    )
    @responses.activate
    def test_create_should_raise_api_errors(
        self,
        client: ProjectsApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.add(
            responses.POST,
            BASE_PROJECTS_URL,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.create(project_name="New Project")

        assert expected_error_message in str(exc_info.value)

    @pytest.mark.parametrize(
        "project_name, expected_errors",
        [
            (None, ["Input should be a valid string"]),
            ("", ["String should have at least 2 characters"]),
            ("a", ["String should have at least 2 characters"]),
            ("a" * 101, ["String should have at most 100 characters"]),
        ],
    )
    def test_create_should_raise_validation_error_on_pydantic_validation(
        self, client: ProjectsApi, project_name: str, expected_errors: list[str]
    ) -> None:
        with pytest.raises(ValidationError) as exc_info:
            client.create(project_name=project_name)

        errors = exc_info.value.errors()
        error_messages = [err["msg"] for err in errors]

        for expected_msg in expected_errors:
            assert any(expected_msg in actual_msg for actual_msg in error_messages)

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

    @pytest.mark.parametrize(
        "status_code,response_json,expected_error_message",
        [
            (401, {"error": "Incorrect API token"}, "Incorrect API token"),
            (403, {"errors": "Access forbidden"}, "Access forbidden"),
            (404, {"error": "Not Found"}, "Not Found"),
        ],
    )
    @responses.activate
    def test_update_should_raise_api_errors(
        self,
        client: ProjectsApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        url = f"{BASE_PROJECTS_URL}/{PROJECT_ID}"
        responses.add(
            responses.PATCH,
            url,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.update(PROJECT_ID, project_name="Update Project Name")

        assert expected_error_message in str(exc_info.value)

    @pytest.mark.parametrize(
        "project_name, expected_errors",
        [
            (None, ["Input should be a valid string"]),
            ("", ["String should have at least 2 characters"]),
            ("a", ["String should have at least 2 characters"]),
            ("a" * 101, ["String should have at most 100 characters"]),
        ],
    )
    def test_update_should_raise_validation_error_on_pydantic_validation(
        self, client: ProjectsApi, project_name: str, expected_errors: list[str]
    ) -> None:
        with pytest.raises(ValidationError) as exc_info:
            client.update(project_id=PROJECT_ID, project_name=project_name)

        errors = exc_info.value.errors()
        error_messages = [err["msg"] for err in errors]

        for expected_msg in expected_errors:
            assert any(expected_msg in actual_msg for actual_msg in error_messages)

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

    @pytest.mark.parametrize(
        "status_code,response_json,expected_error_message",
        [
            (401, {"error": "Incorrect API token"}, "Incorrect API token"),
            (403, {"errors": "Access forbidden"}, "Access forbidden"),
            (404, {"error": "Not Found"}, "Not Found"),
        ],
    )
    @responses.activate
    def test_delete_should_raise_api_errors(
        self,
        client: ProjectsApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        url = f"{BASE_PROJECTS_URL}/{PROJECT_ID}"
        responses.add(
            responses.DELETE,
            url,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.delete(PROJECT_ID)

        assert expected_error_message in str(exc_info.value)

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
