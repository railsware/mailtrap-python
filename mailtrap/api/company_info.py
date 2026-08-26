from mailtrap.api.resources.company_info import CompanyInfoApi
from mailtrap.http import HttpClient


class CompanyInfoBaseApi:
    def __init__(self, client: HttpClient) -> None:
        self._client = client

    @property
    def company_info(self) -> CompanyInfoApi:
        return CompanyInfoApi(client=self._client)
