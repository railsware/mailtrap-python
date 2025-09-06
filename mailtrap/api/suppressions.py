from mailtrap.api.resources.suppressions import SuppressionsApi
from mailtrap.http import HttpClient


class SuppressionsBaseApi:
    def __init__(self, client: HttpClient, account_id: str) -> None:
        self._account_id = account_id
        self._client = client

    @property
    def suppressions(self) -> SuppressionsApi:
        return SuppressionsApi(account_id=self._account_id, client=self._client)
