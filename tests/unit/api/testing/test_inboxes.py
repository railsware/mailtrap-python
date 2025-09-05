from typing import Any

import pytest
import responses

from mailtrap.api.resources.inboxes import InboxesApi
from mailtrap.config import GENERAL_HOST
from mailtrap.exceptions import APIError
from mailtrap.http import HttpClient
from mailtrap.models.inboxes import CreateInboxParams
from mailtrap.models.inboxes import Inbox
from mailtrap.models.inboxes import UpdateInboxParams
from tests import conftest

ACCOUNT_ID = "321"
INBOX_ID = 3538
PROJECT_ID = 2293
BASE_INBOXES_URL = f"https://{GENERAL_HOST}/api/accounts/{ACCOUNT_ID}/inboxes"
BASE_PROJECT_INBOXES_URL = (
    f"https://{GENERAL_HOST}/api/accounts/{ACCOUNT_ID}/projects/{PROJECT_ID}/inboxes"
)


@pytest.fixture
def client() -> InboxesApi:
    return InboxesApi(account_id=ACCOUNT_ID, client=HttpClient(GENERAL_HOST))


@pytest.fixture
def sample_inbox_dict() -> dict[str, Any]:
    return {
        "id": INBOX_ID,
        "name": "Admin Inbox",
        "username": "b3a87978452ae1",
        "password": "6be9fcfc613a7c",
        "max_size": 0,
        "status": "active",
        "email_username": "b7eae548c3-54c542",
        "email_username_enabled": False,
        "sent_messages_count": 52,
        "forwarded_messages_count": 0,
        "used": False,
        "forward_from_email_address": "a3538-i4088@forward.mailtrap.info",
        "project_id": PROJECT_ID,
        "domain": "localhost",
        "pop3_domain": "localhost",
        "email_domain": "localhost",
        "api_domain": "localhost",
        "emails_count": 0,
        "emails_unread_count": 0,
        "last_message_sent_at": None,
        "smtp_ports": [25, 465, 587, 2525],
        "pop3_ports": [1100, 9950],
        "max_message_size": 5242880,
        "permissions": {
            "can_read": True,
            "can_update": True,
            "can_destroy": True,
            "can_leave": True,
        },
    }


class TestInboxesApi:

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
        client: InboxesApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.get(
            BASE_INBOXES_URL,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.get_list()

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_get_list_should_return_inbox_list(
        self, client: InboxesApi, sample_inbox_dict: dict
    ) -> None:
        responses.get(
            BASE_INBOXES_URL,
            json=[sample_inbox_dict],
            status=200,
        )

        inboxes = client.get_list()

        assert isinstance(inboxes, list)
        assert all(isinstance(i, Inbox) for i in inboxes)
        assert inboxes[0].id == INBOX_ID

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
        client: InboxesApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        url = f"{BASE_INBOXES_URL}/{INBOX_ID}"
        responses.get(
            url,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.get_by_id(INBOX_ID)

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_get_by_id_should_return_single_inbox(
        self, client: InboxesApi, sample_inbox_dict: dict
    ) -> None:
        url = f"{BASE_INBOXES_URL}/{INBOX_ID}"
        responses.get(
            url,
            json=sample_inbox_dict,
            status=200,
        )

        inbox = client.get_by_id(INBOX_ID)

        assert isinstance(inbox, Inbox)
        assert inbox.id == INBOX_ID

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
    def test_create_should_raise_api_errors(
        self,
        client: InboxesApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.post(
            BASE_PROJECT_INBOXES_URL,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.create(
                project_id=PROJECT_ID, inbox_params=CreateInboxParams(name="New Inbox")
            )

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_create_should_return_new_inbox(
        self, client: InboxesApi, sample_inbox_dict: dict
    ) -> None:
        responses.post(
            BASE_PROJECT_INBOXES_URL,
            json=sample_inbox_dict,
            status=201,
        )

        inbox = client.create(
            project_id=PROJECT_ID, inbox_params=CreateInboxParams(name="New Inbox")
        )

        assert isinstance(inbox, Inbox)
        assert inbox.name == "Admin Inbox"

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
        client: InboxesApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        url = f"{BASE_INBOXES_URL}/{INBOX_ID}"
        responses.patch(
            url,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            _ = client.update(
                INBOX_ID, inbox_params=UpdateInboxParams(name="Updated Inbox Name")
            )

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_update_should_return_updated_inbox(
        self, client: InboxesApi, sample_inbox_dict: dict
    ) -> None:
        url = f"{BASE_INBOXES_URL}/{INBOX_ID}"
        updated_name = "Updated Inbox"
        updated_inbox_dict = sample_inbox_dict.copy()
        updated_inbox_dict["name"] = updated_name

        responses.patch(
            url,
            json=updated_inbox_dict,
            status=200,
        )

        inbox = client.update(INBOX_ID, inbox_params=UpdateInboxParams(name=updated_name))

        assert isinstance(inbox, Inbox)
        assert inbox.name == updated_name

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
        client: InboxesApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        url = f"{BASE_INBOXES_URL}/{INBOX_ID}"
        responses.delete(
            url,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.delete(INBOX_ID)

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_delete_should_return_deleted_inbox(
        self, client: InboxesApi, sample_inbox_dict: dict
    ) -> None:
        url = f"{BASE_INBOXES_URL}/{INBOX_ID}"
        responses.delete(
            url,
            json=sample_inbox_dict,
            status=200,
        )

        result = client.delete(INBOX_ID)

        assert isinstance(result, Inbox)
        assert result.id == INBOX_ID

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
    def test_clean_should_raise_api_errors(
        self,
        client: InboxesApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        url = f"{BASE_INBOXES_URL}/{INBOX_ID}/clean"
        responses.patch(
            url,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.clean(INBOX_ID)

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_clean_should_return_cleaned_inbox(
        self, client: InboxesApi, sample_inbox_dict: dict
    ) -> None:
        url = f"{BASE_INBOXES_URL}/{INBOX_ID}/clean"
        responses.patch(
            url,
            json=sample_inbox_dict,
            status=200,
        )

        result = client.clean(INBOX_ID)

        assert isinstance(result, Inbox)
        assert result.id == INBOX_ID

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
    def test_mark_as_read_should_raise_api_errors(
        self,
        client: InboxesApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        url = f"{BASE_INBOXES_URL}/{INBOX_ID}/all_read"
        responses.patch(
            url,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.mark_as_read(INBOX_ID)

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_mark_as_read_should_return_inbox(
        self, client: InboxesApi, sample_inbox_dict: dict
    ) -> None:
        url = f"{BASE_INBOXES_URL}/{INBOX_ID}/all_read"
        responses.patch(
            url,
            json=sample_inbox_dict,
            status=200,
        )

        result = client.mark_as_read(INBOX_ID)

        assert isinstance(result, Inbox)
        assert result.id == INBOX_ID

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
    def test_reset_credentials_should_raise_api_errors(
        self,
        client: InboxesApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        url = f"{BASE_INBOXES_URL}/{INBOX_ID}/reset_credentials"
        responses.patch(
            url,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.reset_credentials(INBOX_ID)

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_reset_credentials_should_return_inbox(
        self, client: InboxesApi, sample_inbox_dict: dict
    ) -> None:
        url = f"{BASE_INBOXES_URL}/{INBOX_ID}/reset_credentials"
        responses.patch(
            url,
            json=sample_inbox_dict,
            status=200,
        )

        result = client.reset_credentials(INBOX_ID)

        assert isinstance(result, Inbox)
        assert result.id == INBOX_ID

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
    def test_enable_email_address_should_raise_api_errors(
        self,
        client: InboxesApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        url = f"{BASE_INBOXES_URL}/{INBOX_ID}/toggle_email_username"
        responses.patch(
            url,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.enable_email_address(INBOX_ID)

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_enable_email_address_should_return_inbox(
        self, client: InboxesApi, sample_inbox_dict: dict
    ) -> None:
        url = f"{BASE_INBOXES_URL}/{INBOX_ID}/toggle_email_username"
        responses.patch(
            url,
            json=sample_inbox_dict,
            status=200,
        )

        result = client.enable_email_address(INBOX_ID)

        assert isinstance(result, Inbox)
        assert result.id == INBOX_ID

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
    def test_reset_email_username_should_raise_api_errors(
        self,
        client: InboxesApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        url = f"{BASE_INBOXES_URL}/{INBOX_ID}/reset_email_username"
        responses.patch(
            url,
            status=status_code,
            json=response_json,
        )

        with pytest.raises(APIError) as exc_info:
            client.reset_email_username(INBOX_ID)

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_reset_email_username_should_return_inbox(
        self, client: InboxesApi, sample_inbox_dict: dict
    ) -> None:
        url = f"{BASE_INBOXES_URL}/{INBOX_ID}/reset_email_username"
        responses.patch(
            url,
            json=sample_inbox_dict,
            status=200,
        )

        result = client.reset_email_username(INBOX_ID)

        assert isinstance(result, Inbox)
        assert result.id == INBOX_ID
