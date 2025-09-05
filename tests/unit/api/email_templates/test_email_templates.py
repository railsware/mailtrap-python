from typing import Any

import pytest
import responses

from mailtrap.api.resources.templates import TemplatesApi
from mailtrap.config import GENERAL_HOST
from mailtrap.exceptions import APIError
from mailtrap.http import HttpClient
from mailtrap.models.common import DeletedObject
from mailtrap.models.templates import CreateEmailTemplateParams
from mailtrap.models.templates import EmailTemplate
from mailtrap.models.templates import UpdateEmailTemplateParams
from tests import conftest

ACCOUNT_ID = "321"
TEMPLATE_ID = 26730
BASE_TEMPLATES_URL = f"https://{GENERAL_HOST}/api/accounts/{ACCOUNT_ID}/email_templates"


@pytest.fixture
def client() -> TemplatesApi:
    return TemplatesApi(account_id=ACCOUNT_ID, client=HttpClient(GENERAL_HOST))


@pytest.fixture
def sample_template_dict() -> dict[str, Any]:
    return {
        "id": TEMPLATE_ID,
        "name": "Promotion Template",
        "uuid": "b81aabcd-1a1e-41cf-91b6-eca0254b3d96",
        "category": "Promotion",
        "subject": "Promotion Template subject",
        "body_text": "Text body",
        "body_html": "<div>body</div>",
        "created_at": "2025-01-01T10:00:00Z",
        "updated_at": "2025-01-02T10:00:00Z",
    }


class TestTemplatesApi:

    @pytest.mark.parametrize(
        "status_code,response_json,expected_error_message",
        [
            (
                conftest.UNAUTHORIZED_STATUS_CODE,
                conftest.UNAUTHORIZED_RESPONSE,
                conftest.UNAUTHORIZED_ERROR_MESSAGE,
            ),
            (
                conftest.FORBIDDEN_STATUS_CODE,
                conftest.FORBIDDEN_RESPONSE,
                conftest.FORBIDDEN_ERROR_MESSAGE,
            ),
        ],
    )
    @responses.activate
    def test_get_list_should_raise_api_errors(
        self,
        client: TemplatesApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.get(
            BASE_TEMPLATES_URL,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.get_list()

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_get_list_should_return_templates_list(
        self, client: TemplatesApi, sample_template_dict: dict
    ) -> None:
        responses.get(
            BASE_TEMPLATES_URL,
            json=[sample_template_dict],
            status=200,
        )

        templates = client.get_list()

        assert isinstance(templates, list)
        assert all(isinstance(t, EmailTemplate) for t in templates)
        assert templates[0].id == TEMPLATE_ID

    @pytest.mark.parametrize(
        "status_code,response_json,expected_error_message",
        [
            (
                conftest.UNAUTHORIZED_STATUS_CODE,
                conftest.UNAUTHORIZED_RESPONSE,
                conftest.UNAUTHORIZED_ERROR_MESSAGE,
            ),
            (
                conftest.FORBIDDEN_STATUS_CODE,
                conftest.FORBIDDEN_RESPONSE,
                conftest.FORBIDDEN_ERROR_MESSAGE,
            ),
            (
                conftest.NOT_FOUND_STATUS_CODE,
                conftest.NOT_FOUND_RESPONSE,
                conftest.NOT_FOUND_ERROR_MESSAGE,
            ),
        ],
    )
    @responses.activate
    def test_get_by_id_should_raise_api_errors(
        self,
        client: TemplatesApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        url = f"{BASE_TEMPLATES_URL}/{TEMPLATE_ID}"
        responses.get(
            url,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.get_by_id(TEMPLATE_ID)

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_get_by_id_should_return_single_template(
        self, client: TemplatesApi, sample_template_dict: dict
    ) -> None:
        url = f"{BASE_TEMPLATES_URL}/{TEMPLATE_ID}"
        responses.get(
            url,
            json=sample_template_dict,
            status=200,
        )

        template = client.get_by_id(TEMPLATE_ID)

        assert isinstance(template, EmailTemplate)
        assert template.id == TEMPLATE_ID

    @pytest.mark.parametrize(
        "status_code,response_json,expected_error_message",
        [
            (
                conftest.UNAUTHORIZED_STATUS_CODE,
                conftest.UNAUTHORIZED_RESPONSE,
                conftest.UNAUTHORIZED_ERROR_MESSAGE,
            ),
            (
                conftest.FORBIDDEN_STATUS_CODE,
                conftest.FORBIDDEN_RESPONSE,
                conftest.FORBIDDEN_ERROR_MESSAGE,
            ),
        ],
    )
    @responses.activate
    def test_create_should_raise_api_errors(
        self,
        client: TemplatesApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.post(
            BASE_TEMPLATES_URL,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.create(
                template_params=CreateEmailTemplateParams(
                    name="test", subject="test", category="test"
                )
            )

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_create_should_return_new_template(
        self, client: TemplatesApi, sample_template_dict: dict
    ) -> None:
        responses.post(
            BASE_TEMPLATES_URL,
            json=sample_template_dict,
            status=201,
        )

        template = client.create(
            template_params=CreateEmailTemplateParams(
                name=sample_template_dict["name"],
                subject=sample_template_dict["subject"],
                category=sample_template_dict["category"],
            )
        )

        assert isinstance(template, EmailTemplate)
        assert template.name == sample_template_dict["name"]
        assert template.subject == sample_template_dict["subject"]
        assert template.category == sample_template_dict["category"]
        assert template.uuid == sample_template_dict["uuid"]
        assert template.created_at == sample_template_dict["created_at"]
        assert template.updated_at == sample_template_dict["updated_at"]
        assert template.body_html == sample_template_dict["body_html"]
        assert template.body_text == sample_template_dict["body_text"]

    @pytest.mark.parametrize(
        "status_code,response_json,expected_error_message",
        [
            (
                conftest.UNAUTHORIZED_STATUS_CODE,
                conftest.UNAUTHORIZED_RESPONSE,
                conftest.UNAUTHORIZED_ERROR_MESSAGE,
            ),
            (
                conftest.FORBIDDEN_STATUS_CODE,
                conftest.FORBIDDEN_RESPONSE,
                conftest.FORBIDDEN_ERROR_MESSAGE,
            ),
            (
                conftest.NOT_FOUND_STATUS_CODE,
                conftest.NOT_FOUND_RESPONSE,
                conftest.NOT_FOUND_ERROR_MESSAGE,
            ),
        ],
    )
    @responses.activate
    def test_update_should_raise_api_errors(
        self,
        client: TemplatesApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        url = f"{BASE_TEMPLATES_URL}/{TEMPLATE_ID}"
        responses.patch(
            url,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.update(
                TEMPLATE_ID, template_params=UpdateEmailTemplateParams(name="test")
            )

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_update_should_return_updated_template(
        self, client: TemplatesApi, sample_template_dict: dict
    ) -> None:
        url = f"{BASE_TEMPLATES_URL}/{TEMPLATE_ID}"
        updated_name = "Updated Promotion Template"
        updated_template_dict = sample_template_dict.copy()
        updated_template_dict["name"] = updated_name

        responses.patch(
            url,
            json=updated_template_dict,
            status=200,
        )

        template = client.update(
            TEMPLATE_ID, template_params=UpdateEmailTemplateParams(name=updated_name)
        )

        assert isinstance(template, EmailTemplate)
        assert template.name == updated_name

    @pytest.mark.parametrize(
        "status_code,response_json,expected_error_message",
        [
            (
                conftest.UNAUTHORIZED_STATUS_CODE,
                conftest.UNAUTHORIZED_RESPONSE,
                conftest.UNAUTHORIZED_ERROR_MESSAGE,
            ),
            (
                conftest.FORBIDDEN_STATUS_CODE,
                conftest.FORBIDDEN_RESPONSE,
                conftest.FORBIDDEN_ERROR_MESSAGE,
            ),
            (
                conftest.NOT_FOUND_STATUS_CODE,
                conftest.NOT_FOUND_RESPONSE,
                conftest.NOT_FOUND_ERROR_MESSAGE,
            ),
        ],
    )
    @responses.activate
    def test_delete_should_raise_api_errors(
        self,
        client: TemplatesApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        url = f"{BASE_TEMPLATES_URL}/{TEMPLATE_ID}"
        responses.delete(
            url,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.delete(TEMPLATE_ID)

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_delete_should_return_deleted_object(self, client: TemplatesApi) -> None:
        url = f"{BASE_TEMPLATES_URL}/{TEMPLATE_ID}"
        responses.delete(
            url,
            status=204,
        )

        result = client.delete(TEMPLATE_ID)

        assert isinstance(result, DeletedObject)
        assert result.id == TEMPLATE_ID
