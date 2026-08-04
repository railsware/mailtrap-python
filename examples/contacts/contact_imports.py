import os

import mailtrap as mt
from mailtrap.models.contacts import ContactImport

API_KEY = os.environ["MAILTRAP_API_KEY"]
ACCOUNT_ID = os.environ["MAILTRAP_ACCOUNT_ID"]

client = mt.MailtrapClient(token=API_KEY, account_id=ACCOUNT_ID)
contact_imports_api = client.contacts_api.contact_imports


def import_contacts(contacts: list[mt.ImportContactParams]) -> ContactImport:
    return contact_imports_api.import_contacts(contacts=contacts)


def get_contact_import(import_id: int) -> ContactImport:
    return contact_imports_api.get_by_id(import_id)


if __name__ == "__main__":
    contact_import = import_contacts(
        contacts=[
            mt.ImportContactParams(
                email="testemail@test.com",
                fields={"first_name": "Test", "last_name": "Test"},
            )
        ]
    )
    print(contact_import)

    contact_import = get_contact_import(contact_import.id)
    print(contact_import)
