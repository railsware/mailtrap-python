from typing import Any

import pytest
import responses

from mailtrap.api.resources.contact_fields import ContactFieldsApi
from mailtrap.config import GENERAL_HOST
from mailtrap.exceptions import APIError
from mailtrap.http import HttpClient
from mailtrap.models.common import DeletedObject
from mailtrap.models.contacts import ContactField
from mailtrap.models.contacts import CreateContactFieldParams
from mailtrap.models.contacts import UpdateContactFieldParams
from tests import conftest

ACCOUNT_ID = "321"
FIELD_ID = 6730
BASE_CONTACT_FIELDS_URL = (
    f"https://{GENERAL_HOST}/api/accounts/{ACCOUNT_ID}/contacts/fields"
)
VALIDATION_ERRORS_RESPONSE = {
    "errors": {
        "name": [["is too long (maximum is 80 characters)", "has already been taken"]],
        "merge_tag": [
            ["is too long (maximum is 80 characters)", "has already been taken"]
        ],
    }
}
VALIDATION_ERRORS_MESSAGE = (
    "name: ['is too long (maximum is 80 characters)', 'has already been taken']; "
    "merge_tag: ['is too long (maximum is 80 characters)', 'has already been taken']"
)


@pytest.fixture
def contact_fields_api() -> ContactFieldsApi:
    return ContactFieldsApi(account_id=ACCOUNT_ID, client=HttpClient(GENERAL_HOST))


@pytest.fixture
def sample_contact_field_dict() -> dict[str, Any]:
    return {
        "id": FIELD_ID,
        "name": "First name",
        "data_type": "text",
        "merge_tag": "first_name",
    }


@pytest.fixture
def create_contact_field_params() -> CreateContactFieldParams:
    return CreateContactFieldParams(
        name="My Contact Field", data_type="text", merge_tag="my_contact_field"
    )


@pytest.fixture
def update_contact_field_params() -> UpdateContactFieldParams:
    return UpdateContactFieldParams(name="Updated name", merge_tag="updated_name")


class TestContactsApi:

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
                conftest.RATE_LIMIT_ERROR_STATUS_CODE,
                conftest.RATE_LIMIT_ERROR_RESPONSE,
                conftest.RATE_LIMIT_ERROR_MESSAGE,
            ),
            (
                conftest.INTERNAL_SERVER_ERROR_STATUS_CODE,
                conftest.INTERNAL_SERVER_ERROR_RESPONSE,
                conftest.INTERNAL_SERVER_ERROR_MESSAGE,
            ),
        ],
    )
    @responses.activate
    def test_get_contact_fields_should_raise_api_errors(
        self,
        contact_fields_api: ContactFieldsApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.get(
            BASE_CONTACT_FIELDS_URL,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            contact_fields_api.get_list()

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_get_contact_fields_should_return_contact_field_list(
        self, contact_fields_api: ContactFieldsApi, sample_contact_field_dict: dict
    ) -> None:
        responses.get(
            BASE_CONTACT_FIELDS_URL,
            json=[sample_contact_field_dict],
            status=200,
        )

        contact_fields = contact_fields_api.get_list()

        assert isinstance(contact_fields, list)
        assert all(isinstance(f, ContactField) for f in contact_fields)
        assert contact_fields[0].id == FIELD_ID

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
            (
                conftest.RATE_LIMIT_ERROR_STATUS_CODE,
                conftest.RATE_LIMIT_ERROR_RESPONSE,
                conftest.RATE_LIMIT_ERROR_MESSAGE,
            ),
            (
                conftest.INTERNAL_SERVER_ERROR_STATUS_CODE,
                conftest.INTERNAL_SERVER_ERROR_RESPONSE,
                conftest.INTERNAL_SERVER_ERROR_MESSAGE,
            ),
        ],
    )
    @responses.activate
    def test_get_contact_field_should_raise_api_errors(
        self,
        contact_fields_api: ContactFieldsApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.get(
            f"{BASE_CONTACT_FIELDS_URL}/{FIELD_ID}",
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            contact_fields_api.get_by_id(FIELD_ID)

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_get_contact_field_should_return_contact_field(
        self, contact_fields_api: ContactFieldsApi, sample_contact_field_dict: dict
    ) -> None:
        responses.get(
            f"{BASE_CONTACT_FIELDS_URL}/{FIELD_ID}",
            json=sample_contact_field_dict,
            status=200,
        )

        contact_field = contact_fields_api.get_by_id(FIELD_ID)

        assert isinstance(contact_field, ContactField)
        assert contact_field.id == FIELD_ID
        assert contact_field.name == "First name"
        assert contact_field.data_type == "text"
        assert contact_field.merge_tag == "first_name"

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
                conftest.RATE_LIMIT_ERROR_STATUS_CODE,
                conftest.RATE_LIMIT_ERROR_RESPONSE,
                conftest.RATE_LIMIT_ERROR_MESSAGE,
            ),
            (
                conftest.INTERNAL_SERVER_ERROR_STATUS_CODE,
                conftest.INTERNAL_SERVER_ERROR_RESPONSE,
                conftest.INTERNAL_SERVER_ERROR_MESSAGE,
            ),
            (
                conftest.VALIDATION_ERRORS_STATUS_CODE,
                VALIDATION_ERRORS_RESPONSE,
                VALIDATION_ERRORS_MESSAGE,
            ),
        ],
    )
    @responses.activate
    def test_create_contact_field_should_raise_api_errors(
        self,
        contact_fields_api: ContactFieldsApi,
        create_contact_field_params: CreateContactFieldParams,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.post(
            BASE_CONTACT_FIELDS_URL,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            contact_fields_api.create(create_contact_field_params)

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_create_contact_field_should_return_created_contact_field(
        self,
        contact_fields_api: ContactFieldsApi,
        create_contact_field_params: CreateContactFieldParams,
    ) -> None:
        expected_response = {
            "id": FIELD_ID,
            "name": "My Contact Field",
            "data_type": "text",
            "merge_tag": "my_contact_field",
        }
        responses.post(
            BASE_CONTACT_FIELDS_URL,
            json=expected_response,
            status=201,
        )

        contact_field = contact_fields_api.create(create_contact_field_params)

        assert isinstance(contact_field, ContactField)
        assert contact_field.id == FIELD_ID
        assert contact_field.name == "My Contact Field"
        assert contact_field.data_type == "text"
        assert contact_field.merge_tag == "my_contact_field"

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
            (
                conftest.RATE_LIMIT_ERROR_STATUS_CODE,
                conftest.RATE_LIMIT_ERROR_RESPONSE,
                conftest.RATE_LIMIT_ERROR_MESSAGE,
            ),
            (
                conftest.INTERNAL_SERVER_ERROR_STATUS_CODE,
                conftest.INTERNAL_SERVER_ERROR_RESPONSE,
                conftest.INTERNAL_SERVER_ERROR_MESSAGE,
            ),
            (
                conftest.VALIDATION_ERRORS_STATUS_CODE,
                VALIDATION_ERRORS_RESPONSE,
                VALIDATION_ERRORS_MESSAGE,
            ),
        ],
    )
    @responses.activate
    def test_update_contact_field_should_raise_api_errors(
        self,
        contact_fields_api: ContactFieldsApi,
        update_contact_field_params: UpdateContactFieldParams,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.patch(
            f"{BASE_CONTACT_FIELDS_URL}/{FIELD_ID}",
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            contact_fields_api.update(FIELD_ID, update_contact_field_params)

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_update_contact_field_should_return_updated_contact_field(
        self,
        contact_fields_api: ContactFieldsApi,
        update_contact_field_params: UpdateContactFieldParams,
    ) -> None:
        expected_response = {
            "id": FIELD_ID,
            "name": "Updated name",
            "data_type": "text",
            "merge_tag": "updated_name",
        }
        responses.patch(
            f"{BASE_CONTACT_FIELDS_URL}/{FIELD_ID}",
            json=expected_response,
            status=200,
        )

        contact_field = contact_fields_api.update(FIELD_ID, update_contact_field_params)

        assert isinstance(contact_field, ContactField)
        assert contact_field.id == FIELD_ID
        assert contact_field.name == "Updated name"
        assert contact_field.data_type == "text"
        assert contact_field.merge_tag == "updated_name"

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
            (
                conftest.RATE_LIMIT_ERROR_STATUS_CODE,
                conftest.RATE_LIMIT_ERROR_RESPONSE,
                conftest.RATE_LIMIT_ERROR_MESSAGE,
            ),
            (
                conftest.INTERNAL_SERVER_ERROR_STATUS_CODE,
                conftest.INTERNAL_SERVER_ERROR_RESPONSE,
                conftest.INTERNAL_SERVER_ERROR_MESSAGE,
            ),
            (
                conftest.VALIDATION_ERRORS_STATUS_CODE,
                {
                    "errors": {
                        "usage": [
                            (
                                "This field is used in the steps of automation(s): "
                                "%{automation names}."
                            ),
                            (
                                "This field is used in the conditions of segment(s): "
                                "{segment names}."
                            ),
                        ]
                    }
                },
                (
                    "usage: This field is used in the steps of automation(s): "
                    "%{automation names}.; "
                    "usage: This field is used in the conditions of segment(s): "
                    "{segment names}."
                ),
            ),
        ],
    )
    @responses.activate
    def test_delete_contact_field_should_raise_api_errors(
        self,
        contact_fields_api: ContactFieldsApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.delete(
            f"{BASE_CONTACT_FIELDS_URL}/{FIELD_ID}",
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            contact_fields_api.delete(FIELD_ID)

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_delete_contact_field_should_return_deleted_object(
        self, contact_fields_api: ContactFieldsApi
    ) -> None:
        responses.delete(
            f"{BASE_CONTACT_FIELDS_URL}/{FIELD_ID}",
            status=204,
        )

        deleted_object = contact_fields_api.delete(FIELD_ID)

        assert isinstance(deleted_object, DeletedObject)
        assert deleted_object.id == FIELD_ID
