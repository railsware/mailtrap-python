import mailtrap as mt
from mailtrap.models.common import DeletedObject
from mailtrap.models.inbound import InboundInbox

API_TOKEN = "YOUR_API_TOKEN"
FOLDER_ID = 42

client = mt.MailtrapClient(token=API_TOKEN)
inboxes_api = client.inbound_api.inboxes


def list_inboxes(folder_id: int) -> list[InboundInbox]:
    return inboxes_api.get_list(folder_id)


def get_inbox(folder_id: int, inbox_id: int) -> InboundInbox:
    return inboxes_api.get_by_id(folder_id, inbox_id)


def create_inbox(folder_id: int, name: str) -> InboundInbox:
    # Omit domain_id for a Mailtrap-hosted inbox; pass it for a custom-domain inbox.
    return inboxes_api.create(folder_id, mt.CreateInboundInboxParams(name=name))


def update_inbox(folder_id: int, inbox_id: int, name: str) -> InboundInbox:
    return inboxes_api.update(folder_id, inbox_id, mt.UpdateInboundInboxParams(name=name))


def delete_inbox(folder_id: int, inbox_id: int) -> DeletedObject:
    return inboxes_api.delete(folder_id, inbox_id)


if __name__ == "__main__":
    inbox = create_inbox(FOLDER_ID, "Tickets")
    print(inbox)

    print(list_inboxes(FOLDER_ID))
    print(get_inbox(FOLDER_ID, inbox.id))
    print(update_inbox(FOLDER_ID, inbox.id, "Tickets (renamed)"))
    print(delete_inbox(FOLDER_ID, inbox.id))
