from mailtrap.api.resources.contact_fields import ContactFieldsApi
from mailtrap.http import HttpClient


class ContactsBaseApi:
    def __init__(self, client: HttpClient, account_id: str) -> None:
        self._account_id = account_id
        self._client = client

    @property
    def contact_fields(self) -> ContactFieldsApi:
        return ContactFieldsApi(account_id=self._account_id, client=self._client)
