from typing import Optional

import mailtrap as mt
from mailtrap.models.common import DeletedObject
from mailtrap.models.contacts import ContactField

API_TOKEN = "YOU_API_TOKEN"
ACCOUNT_ID = "YOU_ACCOUNT_ID"

client = mt.MailtrapClient(token=API_TOKEN, account_id=ACCOUNT_ID)
contact_fields_api = client.contacts_api.contact_fields


def create_contact_field(
    name: str,
    data_type: str,
    merge_tag: str,
) -> ContactField:
    params = mt.CreateContactFieldParams(
        name=name,
        data_type=data_type,
        merge_tag=merge_tag,
    )
    return contact_fields_api.create(params)


def update_contact_field(
    contact_field_id: int,
    name: Optional[str] = None,
    merge_tag: Optional[str] = None,
) -> ContactField:
    params = mt.UpdateContactFieldParams(name=name, merge_tag=merge_tag)
    return contact_fields_api.update(contact_field_id, params)


def list_contact_fields() -> list[ContactField]:
    return contact_fields_api.get_list()


def get_contact_field(contact_field_id: int) -> ContactField:
    return contact_fields_api.get_by_id(contact_field_id)


def delete_contact_field(contact_field_id: int) -> DeletedObject:
    return contact_fields_api.delete(contact_field_id)


if __name__ == "__main__":
    print(list_contact_fields())
