from mailtrap.http import HttpClient
from mailtrap.models.common import DeletedObject
from mailtrap.models.contacts import ContactField
from mailtrap.models.contacts import CreateContactFieldParams
from mailtrap.models.contacts import UpdateContactFieldParams


class ContactFieldsApi:
    def __init__(self, client: HttpClient, account_id: str) -> None:
        self._account_id = account_id
        self._client = client

    def get_list(self) -> list[ContactField]:
        response = self._client.get(f"/api/accounts/{self._account_id}/contacts/fields")
        return [ContactField(**field) for field in response]

    def get_by_id(self, field_id: int) -> ContactField:
        response = self._client.get(
            f"/api/accounts/{self._account_id}/contacts/fields/{field_id}"
        )
        return ContactField(**response)

    def create(self, field_params: CreateContactFieldParams) -> ContactField:
        response = self._client.post(
            f"/api/accounts/{self._account_id}/contacts/fields",
            json=field_params.api_data,
        )
        return ContactField(**response)

    def update(
        self, field_id: int, field_params: UpdateContactFieldParams
    ) -> ContactField:
        response = self._client.patch(
            f"/api/accounts/{self._account_id}/contacts/fields/{field_id}",
            json=field_params.api_data,
        )
        return ContactField(**response)

    def delete(self, field_id: int) -> DeletedObject:
        self._client.delete(
            f"/api/accounts/{self._account_id}/contacts/fields/{field_id}"
        )
        return DeletedObject(field_id)
