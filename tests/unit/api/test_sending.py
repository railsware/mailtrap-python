import json

import pytest
import responses

import mailtrap as mt
from mailtrap.api.sending import SendingApi
from mailtrap.config import SENDING_HOST
from mailtrap.http import HttpClient
from mailtrap.models.mail.base import SendingMailResponse

ACCOUNT_ID = "321"
PROJECT_ID = 123
INBOX_ID = "456"

DUMMY_ADDRESS = mt.Address(email="joe@mail.com")
DUMMY_MAIL = mt.Mail(
    sender=DUMMY_ADDRESS,
    to=[DUMMY_ADDRESS],
    subject="Email subject",
    text="email text",
)
DUMMY_MAIL_FROM_TEMPLATE = mt.MailFromTemplate(
    sender=DUMMY_ADDRESS,
    to=[DUMMY_ADDRESS],
    template_uuid="fake_uuid",
)

MAIL_ENTITIES = [DUMMY_MAIL, DUMMY_MAIL_FROM_TEMPLATE]

SEND_FULL_URL = f"https://{SENDING_HOST}/api/send"


def get_sending_api() -> SendingApi:
    return SendingApi(client=HttpClient(SENDING_HOST))


class TestSendingApi:

    @responses.activate
    @pytest.mark.parametrize("mail", MAIL_ENTITIES)
    def test_send_should_raise_authorization_error(
        self,
        mail: mt.BaseMail,
    ) -> None:
        response_body = {"errors": ["Unauthorized"]}
        responses.post(SEND_FULL_URL, json=response_body, status=401)
        api = get_sending_api()

        with pytest.raises(mt.AuthorizationError):
            api.send(mail)

    @responses.activate
    @pytest.mark.parametrize("mail", MAIL_ENTITIES)
    def test_send_should_raise_api_error_for_400_status_code(
        self,
        mail: mt.BaseMail,
    ) -> None:
        response_body = {"errors": ["Some error msg"]}
        responses.post(SEND_FULL_URL, json=response_body, status=400)

        api = get_sending_api()

        with pytest.raises(mt.APIError):
            api.send(mail)

    @responses.activate
    @pytest.mark.parametrize("mail", MAIL_ENTITIES)
    def test_send_should_raise_api_error_for_500_status_code(
        self,
        mail: mt.BaseMail,
    ) -> None:
        response_body = {"errors": ["Some error msg"]}
        responses.post(SEND_FULL_URL, json=response_body, status=500)

        api = get_sending_api()

        with pytest.raises(mt.APIError):
            api.send(mail)

    @responses.activate
    @pytest.mark.parametrize("mail", MAIL_ENTITIES)
    def test_send_should_handle_success_response(
        self,
        mail: mt.BaseMail,
    ) -> None:
        response_body = {"success": True, "message_ids": ["12345"]}
        responses.post(SEND_FULL_URL, json=response_body)

        api = get_sending_api()
        result = api.send(mail)

        assert isinstance(result, SendingMailResponse)
        assert result.success is True
        assert len(responses.calls) == 1
        request = responses.calls[0].request  # type: ignore
        assert request.body == json.dumps(mail.api_data).encode()
