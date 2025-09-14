from typing import Optional

import mailtrap as mt
from mailtrap.models.messages import AnalysisReport
from mailtrap.models.messages import EmailMessage
from mailtrap.models.messages import ForwardedMessage
from mailtrap.models.messages import SpamReport

API_TOKEN = "YOU_API_TOKEN"
ACCOUNT_ID = "YOU_ACCOUNT_ID"
INBOX_ID = "YOUR_INBOX_ID"

client = mt.MailtrapClient(token=API_TOKEN, account_id=ACCOUNT_ID)
messages_api = client.testing_api.messages


def get_message(inbox_id: int, message_id: int) -> EmailMessage:
    return messages_api.show_message(inbox_id=inbox_id, message_id=message_id)


def update_message(inbox_id: int, message_id: int, is_read: bool) -> EmailMessage:
    return messages_api.update(
        inbox_id=inbox_id,
        message_id=message_id,
        message_params=mt.UpdateEmailMessageParams(is_read=is_read),
    )


def delete_message(inbox_id: int, message_id: int) -> EmailMessage:
    return messages_api.delete(inbox_id=inbox_id, message_id=message_id)


def list_messages(
    inbox_id: int,
    search: Optional[str] = None,
    last_id: Optional[int] = None,
    page: Optional[int] = None,
) -> list[EmailMessage]:
    return messages_api.get_list(
        inbox_id=inbox_id, search=search, last_id=last_id, page=page
    )


def forward_message(inbox_id: int, message_id: int, email: str) -> ForwardedMessage:
    return messages_api.forward(inbox_id=inbox_id, message_id=message_id, email=email)


def get_spam_report(inbox_id: int, message_id: str) -> SpamReport:
    return messages_api.get_spam_report(inbox_id=inbox_id, message_id=message_id)


def get_html_analysis(inbox_id: int, message_id: str) -> AnalysisReport:
    return messages_api.get_html_analysis(inbox_id=inbox_id, message_id=message_id)


def get_text_body(inbox_id: int, message_id: str) -> str:
    return messages_api.get_text_body(inbox_id=inbox_id, message_id=message_id)


def get_raw_body(inbox_id: int, message_id: str) -> str:
    return messages_api.get_raw_body(inbox_id=inbox_id, message_id=message_id)


def get_html_source(inbox_id: int, message_id: str) -> str:
    return messages_api.get_html_source(inbox_id=inbox_id, message_id=message_id)


def get_html_body(inbox_id: int, message_id: str) -> str:
    return messages_api.get_html_body(inbox_id=inbox_id, message_id=message_id)


def get_eml_body(inbox_id: int, message_id: str) -> str:
    return messages_api.get_eml_body(inbox_id=inbox_id, message_id=message_id)


def get_mail_headers(inbox_id: int, message_id: str) -> str:
    return messages_api.get_mail_headers(inbox_id=inbox_id, message_id=message_id)


if __name__ == "__main__":
    messages = list_messages(inbox_id=INBOX_ID)
    print(messages)
