import pytest
import responses

from mailtrap.api.resources.inbound_messages import InboundMessagesApi
from mailtrap.config import GENERAL_HOST
from mailtrap.exceptions import APIError
from mailtrap.http import HttpClient
from mailtrap.models.common import DeletedObject
from mailtrap.models.inbound import ForwardInboundMessageParams
from mailtrap.models.inbound import InboundMessageDetails
from mailtrap.models.inbound import InboundMessagesListResponse
from mailtrap.models.inbound import InboundSendResult
from mailtrap.models.inbound import ReplyInboundMessageParams
from mailtrap.models.mail.address import Address
from tests import conftest

INBOX_ID = 9
MESSAGE_ID = "1871574677877796928"
BASE_URL = f"https://{GENERAL_HOST}/api/inbound/inboxes/{INBOX_ID}/messages"


@pytest.fixture
def messages_api() -> InboundMessagesApi:
    return InboundMessagesApi(client=HttpClient(GENERAL_HOST))


class TestInboundMessagesApi:

    @responses.activate
    def test_get_list_should_return_page(self, messages_api: InboundMessagesApi) -> None:
        responses.get(
            BASE_URL,
            json={
                "data": [
                    {
                        "id": MESSAGE_ID,
                        "inbox_id": INBOX_ID,
                        "from": "customer@example.com",
                        "subject": "Question",
                        "received_at": "2026-01-15T10:30:00Z",
                    }
                ],
                "total_count": 1,
                "last_id": MESSAGE_ID,
            },
            status=200,
        )

        page = messages_api.get_list(INBOX_ID)

        assert isinstance(page, InboundMessagesListResponse)
        assert page.total_count == 1
        assert page.last_id == MESSAGE_ID
        assert page.data[0].from_ == "customer@example.com"

    @responses.activate
    def test_get_list_should_pass_last_id_cursor(
        self, messages_api: InboundMessagesApi
    ) -> None:
        responses.get(
            BASE_URL, json={"data": [], "total_count": 0, "last_id": None}, status=200
        )

        messages_api.get_list(INBOX_ID, last_id="cursor-1")

        assert "last_id=cursor-1" in responses.calls[-1].request.url

    @responses.activate
    def test_get_by_id_should_return_details(
        self, messages_api: InboundMessagesApi
    ) -> None:
        responses.get(
            f"{BASE_URL}/{MESSAGE_ID}",
            json={
                "id": MESSAGE_ID,
                "inbox_id": INBOX_ID,
                "from": "customer@example.com",
                "received_at": "2026-01-15T10:30:00Z",
                "html_body": "<p>Hi</p>",
                "attachments": [{"attachment_id": "a1", "download_url": "https://x/a1"}],
            },
            status=200,
        )

        message = messages_api.get_by_id(INBOX_ID, MESSAGE_ID)

        assert isinstance(message, InboundMessageDetails)
        assert message.html_body == "<p>Hi</p>"
        assert message.attachments[0].download_url == "https://x/a1"

    @responses.activate
    def test_delete_should_return_deleted_object(
        self, messages_api: InboundMessagesApi
    ) -> None:
        responses.delete(f"{BASE_URL}/{MESSAGE_ID}", status=204)

        deleted = messages_api.delete(INBOX_ID, MESSAGE_ID)

        assert isinstance(deleted, DeletedObject)
        assert deleted.id == MESSAGE_ID

    @responses.activate
    def test_reply_should_send_flat_body_and_return_result(
        self, messages_api: InboundMessagesApi
    ) -> None:
        responses.post(
            f"{BASE_URL}/{MESSAGE_ID}/reply",
            json={"message_ids": ["s1"]},
            status=200,
        )

        result = messages_api.reply(
            INBOX_ID, MESSAGE_ID, ReplyInboundMessageParams(text="Thanks!")
        )

        assert isinstance(result, InboundSendResult)
        assert result.message_ids == ["s1"]
        assert responses.calls[-1].request.body == b'{"text": "Thanks!"}'

    @responses.activate
    def test_reply_all_should_return_result(
        self, messages_api: InboundMessagesApi
    ) -> None:
        responses.post(
            f"{BASE_URL}/{MESSAGE_ID}/reply_all",
            json={"message_ids": ["s1", "s2"]},
            status=200,
        )

        result = messages_api.reply_all(
            INBOX_ID, MESSAGE_ID, ReplyInboundMessageParams(text="All")
        )

        assert result.message_ids == ["s1", "s2"]

    @responses.activate
    def test_forward_should_serialize_recipients_and_return_result(
        self, messages_api: InboundMessagesApi
    ) -> None:
        responses.post(
            f"{BASE_URL}/{MESSAGE_ID}/forward",
            json={"message_ids": ["s1"]},
            status=200,
        )

        params = ForwardInboundMessageParams(to=[Address(email="colleague@example.com")])
        result = messages_api.forward(INBOX_ID, MESSAGE_ID, params)

        assert result.message_ids == ["s1"]
        assert (
            responses.calls[-1].request.body
            == b'{"to": [{"email": "colleague@example.com"}]}'
        )

    @pytest.mark.parametrize(
        "status_code,response_json,expected_error_message",
        [
            (
                conftest.UNAUTHORIZED_STATUS_CODE,
                conftest.UNAUTHORIZED_RESPONSE,
                conftest.UNAUTHORIZED_ERROR_MESSAGE,
            ),
            (
                conftest.NOT_FOUND_STATUS_CODE,
                conftest.NOT_FOUND_RESPONSE,
                conftest.NOT_FOUND_ERROR_MESSAGE,
            ),
        ],
    )
    @responses.activate
    def test_reply_should_raise_api_errors(
        self,
        messages_api: InboundMessagesApi,
        status_code: int,
        response_json: dict,
        expected_error_message: str,
    ) -> None:
        responses.post(
            f"{BASE_URL}/{MESSAGE_ID}/reply", status=status_code, json=response_json
        )

        with pytest.raises(APIError) as exc_info:
            messages_api.reply(
                INBOX_ID, MESSAGE_ID, ReplyInboundMessageParams(text="Thanks!")
            )

        assert expected_error_message in str(exc_info.value)
