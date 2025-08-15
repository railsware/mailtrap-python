from typing import Union
from typing import cast

from mailtrap.http import HttpClient
from mailtrap.models.mail.base import BaseMail

SEND_ENDPOINT_RESPONSE = dict[str, Union[bool, list[str]]]


class SendingApi:
    def __init__(self, api_url: str, client: HttpClient) -> None:
        self._api_url = api_url
        self._client = client

    def send(self, mail: BaseMail) -> SEND_ENDPOINT_RESPONSE:
        return cast(
            SEND_ENDPOINT_RESPONSE, self._client.post(self._api_url, json=mail.api_data)
        )
