from typing import Optional

from mailtrap.http import HttpClient
from mailtrap.models.common import DeletedObject
from mailtrap.models.contacts import ContactList
from mailtrap.models.contacts import ContactListParams


class ContactListsApi:
    def __init__(self, client: HttpClient, account_id: str) -> None:
        self._account_id = account_id
        self._client = client

    def get_list(self) -> list[ContactList]:
        response = self._client.get(self._api_path())
        return [ContactList(**field) for field in response]

    def get_by_id(self, list_id: int) -> ContactList:
        response = self._client.get(self._api_path(list_id))
        return ContactList(**response)

    def create(self, list_params: ContactListParams) -> ContactList:
        response = self._client.post(
            self._api_path(),
            json=list_params.api_data,
        )
        return ContactList(**response)

    def update(self, list_id: int, list_params: ContactListParams) -> ContactList:
        response = self._client.patch(
            self._api_path(list_id),
            json=list_params.api_data,
        )
        return ContactList(**response)

    def delete(self, list_id: int) -> DeletedObject:
        self._client.delete(self._api_path(list_id))
        return DeletedObject(list_id)

    def _api_path(self, list_id: Optional[int] = None) -> str:
        path = f"/api/accounts/{self._account_id}/contacts/lists"
        if list_id is not None:
            return f"{path}/{list_id}"
        return path
