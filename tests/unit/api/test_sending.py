import json
from typing import Callable

import pytest
import responses

import mailtrap as mt
from mailtrap.api.sending import DefaultSendingApi
from mailtrap.api.sending import SandboxSendingApi
from mailtrap.api.sending import SendingApi
from mailtrap.config import SANDBOX_HOST
from mailtrap.config import SENDING_HOST
from mailtrap.http import HttpClient

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
SANDBOX_SEND_FULL_URL = f"https://{SANDBOX_HOST}/api/send/{INBOX_ID}"


def get_sending_api() -> SendingApi:
    return DefaultSendingApi(client=HttpClient(SENDING_HOST))


def get_sandbox_sending_api() -> SendingApi:
    return SandboxSendingApi(inbox_id=INBOX_ID, client=HttpClient(SANDBOX_HOST))


SENDING_API_FACTORIES = [
    (get_sending_api, SEND_FULL_URL),
    (get_sandbox_sending_api, SANDBOX_SEND_FULL_URL),
]


class TestSendingApi:

    @responses.activate
    @pytest.mark.parametrize("mail", MAIL_ENTITIES)
    @pytest.mark.parametrize("api_factory,full_url", SENDING_API_FACTORIES)
    def test_send_should_raise_authorization_error(
        self,
        mail: mt.BaseMail,
        api_factory: Callable[[], SendingApi],
        full_url: str,
    ) -> None:
        response_body = {"errors": ["Unauthorized"]}
        responses.post(full_url, json=response_body, status=401)

        api = api_factory()

        with pytest.raises(mt.AuthorizationError):
            api.send(mail)

    @responses.activate
    @pytest.mark.parametrize("mail", MAIL_ENTITIES)
    @pytest.mark.parametrize("api_factory,full_url", SENDING_API_FACTORIES)
    def test_send_should_raise_api_error_for_400_status_code(
        self,
        mail: mt.BaseMail,
        api_factory: Callable[[], SendingApi],
        full_url: str,
    ) -> None:
        response_body = {"errors": ["Some error msg"]}
        responses.post(full_url, json=response_body, status=400)

        api = api_factory()

        with pytest.raises(mt.APIError):
            api.send(mail)

    @responses.activate
    @pytest.mark.parametrize("mail", MAIL_ENTITIES)
    @pytest.mark.parametrize("api_factory,full_url", SENDING_API_FACTORIES)
    def test_send_should_raise_api_error_for_500_status_code(
        self,
        mail: mt.BaseMail,
        api_factory: Callable[[], SendingApi],
        full_url: str,
    ) -> None:
        response_body = {"errors": ["Some error msg"]}
        responses.post(full_url, json=response_body, status=500)

        api = api_factory()

        with pytest.raises(mt.APIError):
            api.send(mail)

    @responses.activate
    @pytest.mark.parametrize("mail", MAIL_ENTITIES)
    @pytest.mark.parametrize("api_factory,full_url", SENDING_API_FACTORIES)
    def test_send_should_handle_success_response(
        self,
        mail: mt.BaseMail,
        api_factory: Callable[[], SendingApi],
        full_url: str,
    ) -> None:
        response_body = {"success": True, "message_ids": ["12345"]}
        responses.post(full_url, json=response_body)

        api = api_factory()
        result = api.send(mail)

        assert result == response_body
        assert len(responses.calls) == 1
        request = responses.calls[0].request  # type: ignore
        assert request.body == json.dumps(mail.api_data).encode()
