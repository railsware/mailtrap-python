import os

import mailtrap as mt
from mailtrap.models.attachments import Attachment

API_KEY = os.environ["MAILTRAP_API_KEY"]
ACCOUNT_ID = os.environ["MAILTRAP_ACCOUNT_ID"]
INBOX_ID = os.environ["MAILTRAP_INBOX_ID"]
MESSAGE_ID = os.environ["MAILTRAP_SANDBOX_MESSAGE_ID"]

client = mt.MailtrapClient(token=API_KEY, account_id=ACCOUNT_ID)
attachments_api = client.testing_api.attachments


def list_attachments(inbox_id: int, message_id: int) -> list[Attachment]:
    return attachments_api.get_list(inbox_id=inbox_id, message_id=message_id)


def get_attachment(inbox_id: int, message_id: int, attachment_id: int) -> Attachment:
    return attachments_api.get(
        inbox_id=inbox_id,
        message_id=message_id,
        attachment_id=attachment_id,
    )


if __name__ == "__main__":
    attachments = list_attachments(inbox_id=INBOX_ID, message_id=MESSAGE_ID)
    print(attachments)
    if attachments:
        attachment = get_attachment(
            inbox_id=INBOX_ID, message_id=MESSAGE_ID, attachment_id=attachments[0].id
        )
        print(attachment)
