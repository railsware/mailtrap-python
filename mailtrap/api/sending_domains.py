from mailtrap.api.resources.company_info import CompanyInfoApi
from mailtrap.api.resources.sending_domains import SendingDomainsApi
from mailtrap.http import HttpClient


class SendingDomainsBaseApi:
    def __init__(self, client: HttpClient, account_id: str) -> None:
        self._account_id = account_id
        self._client = client

    @property
    def sending_domains(self) -> SendingDomainsApi:
        return SendingDomainsApi(account_id=self._account_id, client=self._client)

    @property
    def company_info(self) -> CompanyInfoApi:
        return CompanyInfoApi(account_id=self._account_id, client=self._client)
