from typing import Protocol
from typing import Union
from typing import cast

from mailtrap.http import HttpClient
from mailtrap.models.mail.base import BaseMail

SEND_ENDPOINT_RESPONSE = dict[str, Union[bool, list[str]]]


class SendingApi(Protocol):
    def send(self, mail: BaseMail) -> SEND_ENDPOINT_RESPONSE: ...


class DefaultSendingApi:
    def __init__(self, client: HttpClient) -> None:
        self._client = client

    def send(self, mail: BaseMail) -> SEND_ENDPOINT_RESPONSE:
        return cast(
            SEND_ENDPOINT_RESPONSE, self._client.post("/api/send", json=mail.api_data)
        )


class SandboxSendingApi:
    def __init__(self, inbox_id: str, client: HttpClient) -> None:
        self.inbox_id = inbox_id
        self._client = client

    def send(self, mail: BaseMail) -> SEND_ENDPOINT_RESPONSE:
        return cast(
            SEND_ENDPOINT_RESPONSE,
            self._client.post(f"/api/send/{self.inbox_id}", json=mail.api_data),
        )
