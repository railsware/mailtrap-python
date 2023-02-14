import json
from typing import Any

import pytest
import responses

import mailtrap as mt

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


class TestMailtrapClient:
    SEND_URL = "https://send.api.mailtrap.io:443/api/send"

    @staticmethod
    def get_client(**kwargs: Any) -> mt.MailtrapClient:
        props = {"token": "fake_token", **kwargs}
        return mt.MailtrapClient(**props)

    def test_base_url_should_truncate_slash_from_host(self) -> None:
        client = self.get_client(api_host="example.send.com/", api_port=543)

        assert client.base_url == "https://example.send.com:543"

    def test_headers_should_return_appropriate_dict(self) -> None:
        client = self.get_client()

        assert client.headers == {
            "Authorization": "Bearer fake_token",
            "Content-Type": "application/json",
        }

    @responses.activate
    @pytest.mark.parametrize("mail", MAIL_ENTITIES)
    def test_send_should_handle_success_response(self, mail: mt.BaseMail) -> None:
        response_body = {"success": True, "message_ids": ["12345"]}
        responses.add(responses.POST, self.SEND_URL, json=response_body)

        client = self.get_client()
        result = client.send(mail)

        assert result == response_body
        assert len(responses.calls) == 1
        request = responses.calls[0].request  # type: ignore
        assert request.headers.items() >= client.headers.items()
        assert request.body == json.dumps(mail.api_data).encode()

    @responses.activate
    @pytest.mark.parametrize("mail", MAIL_ENTITIES)
    def test_send_should_raise_authorization_error(self, mail: mt.BaseMail) -> None:
        response_body = {"errors": ["Unauthorized"]}
        responses.add(responses.POST, self.SEND_URL, json=response_body, status=401)

        client = self.get_client()

        with pytest.raises(mt.AuthorizationError):
            client.send(mail)

    @responses.activate
    @pytest.mark.parametrize("mail", MAIL_ENTITIES)
    def test_send_should_raise_api_error_for_400_status_code(
        self, mail: mt.BaseMail
    ) -> None:
        response_body = {"errors": ["Some error msg"]}
        responses.add(responses.POST, self.SEND_URL, json=response_body, status=400)

        client = self.get_client()

        with pytest.raises(mt.APIError):
            client.send(mail)

    @responses.activate
    @pytest.mark.parametrize("mail", MAIL_ENTITIES)
    def test_send_should_raise_api_error_for_500_status_code(
        self, mail: mt.BaseMail
    ) -> None:
        response_body = {"errors": ["Some error msg"]}
        responses.add(responses.POST, self.SEND_URL, json=response_body, status=500)

        client = self.get_client()

        with pytest.raises(mt.APIError):
            client.send(mail)
