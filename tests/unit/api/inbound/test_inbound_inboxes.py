import pytest
import responses

from mailtrap.api.resources.inbound_inboxes import InboundInboxesApi
from mailtrap.config import GENERAL_HOST
from mailtrap.exceptions import APIError
from mailtrap.http import HttpClient
from mailtrap.models.common import DeletedObject
from mailtrap.models.inbound import CreateInboundInboxParams
from mailtrap.models.inbound import InboundInbox
from mailtrap.models.inbound import UpdateInboundInboxParams
from tests import conftest

FOLDER_ID = 42
INBOX_ID = 9
BASE_URL = f"https://{GENERAL_HOST}/api/inbound/folders/{FOLDER_ID}/inboxes"


def _inbox_dict() -> dict:
    return {
        "id": INBOX_ID,
        "name": "Tickets",
        "address": "tickets@inbound.example.com",
        "domain_id": 3,
    }


@pytest.fixture
def inboxes_api() -> InboundInboxesApi:
    return InboundInboxesApi(client=HttpClient(GENERAL_HOST))


class TestInboundInboxesApi:

    @responses.activate
    def test_get_list_should_return_inboxes(self, inboxes_api: InboundInboxesApi) -> None:
        responses.get(BASE_URL, json=[_inbox_dict()], status=200)

        inboxes = inboxes_api.get_list(FOLDER_ID)

        assert all(isinstance(i, InboundInbox) for i in inboxes)
        assert inboxes[0].id == INBOX_ID
        assert inboxes[0].address == "tickets@inbound.example.com"

    @responses.activate
    def test_get_by_id_should_return_inbox(self, inboxes_api: InboundInboxesApi) -> None:
        responses.get(f"{BASE_URL}/{INBOX_ID}", json=_inbox_dict(), status=200)

        inbox = inboxes_api.get_by_id(FOLDER_ID, INBOX_ID)

        assert isinstance(inbox, InboundInbox)
        assert inbox.domain_id == 3

    @responses.activate
    def test_create_should_send_flat_body_and_return_inbox(
        self, inboxes_api: InboundInboxesApi
    ) -> None:
        responses.post(BASE_URL, json=_inbox_dict(), status=200)

        params = CreateInboundInboxParams(name="Tickets", domain_id=3)
        inbox = inboxes_api.create(FOLDER_ID, params)

        assert inbox.id == INBOX_ID
        assert responses.calls[-1].request.body == b'{"name": "Tickets", "domain_id": 3}'

    @responses.activate
    def test_create_should_omit_domain_id_when_not_set(
        self, inboxes_api: InboundInboxesApi
    ) -> None:
        responses.post(BASE_URL, json=_inbox_dict(), status=200)

        inboxes_api.create(FOLDER_ID, CreateInboundInboxParams(name="Tickets"))

        assert responses.calls[-1].request.body == b'{"name": "Tickets"}'

    @pytest.mark.parametrize(
        "status_code,response_json,expected_error_message",
        [
            (
                conftest.UNAUTHORIZED_STATUS_CODE,
                conftest.UNAUTHORIZED_RESPONSE,
                conftest.UNAUTHORIZED_ERROR_MESSAGE,
            ),
            (
                conftest.VALIDATION_ERRORS_STATUS_CODE,
                {"errors": {"name": ["can't be blank"]}},
                "name: can't be blank",
            ),
        ],
    )
    @responses.activate
    def test_create_should_raise_api_errors(
        self,
        inboxes_api: InboundInboxesApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.post(BASE_URL, status=status_code, json=response_json)

        with pytest.raises(APIError) as exc_info:
            inboxes_api.create(FOLDER_ID, CreateInboundInboxParams(name=""))

        assert expected_error_message in str(exc_info.value)

    @responses.activate
    def test_update_should_return_inbox(self, inboxes_api: InboundInboxesApi) -> None:
        responses.patch(f"{BASE_URL}/{INBOX_ID}", json=_inbox_dict(), status=200)

        inbox = inboxes_api.update(
            FOLDER_ID, INBOX_ID, UpdateInboundInboxParams(name="Tickets")
        )

        assert inbox.id == INBOX_ID

    @responses.activate
    def test_delete_should_return_deleted_object(
        self, inboxes_api: InboundInboxesApi
    ) -> None:
        responses.delete(f"{BASE_URL}/{INBOX_ID}", status=204)

        deleted = inboxes_api.delete(FOLDER_ID, INBOX_ID)

        assert isinstance(deleted, DeletedObject)
        assert deleted.id == INBOX_ID
