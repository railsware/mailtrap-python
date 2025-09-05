from typing import Optional

from mailtrap.http import HttpClient
from mailtrap.models.mail.base import BaseMail
from mailtrap.models.mail.base import SendingMailResponse


class SendingApi:
    def __init__(self, client: HttpClient, inbox_id: Optional[str] = None) -> None:
        self._inbox_id = inbox_id
        self._client = client

    @property
    def _api_url(self) -> str:
        url = "/api/send"
        if self._inbox_id:
            return f"{url}/{self._inbox_id}"
        return url

    def send(self, mail: BaseMail) -> SendingMailResponse:
        """Send email (text, html, text&html, templates)."""
        response = self._client.post(self._api_url, json=mail.api_data)
        return SendingMailResponse(**response)
