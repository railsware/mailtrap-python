import mailtrap as mt
from mailtrap.models.common import DeletedObject
from mailtrap.models.inbound import InboundMessageDetails
from mailtrap.models.inbound import InboundMessagesListResponse
from mailtrap.models.inbound import InboundSendResult
from mailtrap.models.mail.address import Address

API_TOKEN = "YOUR_API_TOKEN"
INBOX_ID = 9

client = mt.MailtrapClient(token=API_TOKEN)
messages_api = client.inbound_api.messages


def list_messages(inbox_id: int) -> InboundMessagesListResponse:
    # Pass last_id from the previous page to paginate.
    return messages_api.get_list(inbox_id)


def get_message(inbox_id: int, message_id: str) -> InboundMessageDetails:
    return messages_api.get_by_id(inbox_id, message_id)


def delete_message(inbox_id: int, message_id: str) -> DeletedObject:
    return messages_api.delete(inbox_id, message_id)


def reply(inbox_id: int, message_id: str, text: str) -> InboundSendResult:
    params = mt.ReplyInboundMessageParams(text=text)
    return messages_api.reply(inbox_id, message_id, params)


def reply_all(inbox_id: int, message_id: str, text: str) -> InboundSendResult:
    params = mt.ReplyInboundMessageParams(text=text)
    return messages_api.reply_all(inbox_id, message_id, params)


def forward(inbox_id: int, message_id: str, to: str) -> InboundSendResult:
    params = mt.ForwardInboundMessageParams(to=[Address(email=to)])
    return messages_api.forward(inbox_id, message_id, params)


if __name__ == "__main__":
    page = list_messages(INBOX_ID)
    print(f"{len(page.data)} of {page.total_count} messages")

    if page.data:
        message_id = page.data[0].id
        print(get_message(INBOX_ID, message_id))
        print(reply(INBOX_ID, message_id, "Thanks for reaching out!"))
        print(reply_all(INBOX_ID, message_id, "Looping everyone in."))
        print(forward(INBOX_ID, message_id, "colleague@example.com"))
        print(delete_message(INBOX_ID, message_id))
