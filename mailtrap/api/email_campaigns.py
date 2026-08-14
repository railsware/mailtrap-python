from mailtrap.api.resources.email_campaigns import EmailCampaignsApi
from mailtrap.http import HttpClient


class EmailCampaignsBaseApi:
    def __init__(self, client: HttpClient) -> None:
        self._client = client

    @property
    def email_campaigns(self) -> EmailCampaignsApi:
        return EmailCampaignsApi(client=self._client)
