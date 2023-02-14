from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from mailtrap.mail.address import Address
from mailtrap.mail.attachment import Attachment
from mailtrap.mail.base import BaseMail


class Mail(BaseMail):
    """Creates a request body for /api/send Mailtrap API v2 endpoint.

    Either `text` or `html` param must be specified. You can also
    provide both of them.

    If only `text` is provided, `EmailWithText` body type will be used.
    If only `html` is provided, `HtmlWithText` body type will be used.
    If both `text` and `html` are provided,
        `EmailWithTextAndHtml` body type will be used.
    """

    def __init__(
        self,
        sender: Address,
        to: List[Address],
        subject: str,
        text: Optional[str] = None,
        html: Optional[str] = None,
        category: Optional[str] = None,
        cc: Optional[List[Address]] = None,
        bcc: Optional[List[Address]] = None,
        attachments: Optional[List[Attachment]] = None,
        headers: Optional[Dict[str, str]] = None,
        custom_variables: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            sender=sender,
            to=to,
            cc=cc,
            bcc=bcc,
            attachments=attachments,
            headers=headers,
            custom_variables=custom_variables,
        )
        self.subject = subject
        self.text = text
        self.html = html
        self.category = category

    @property
    def api_data(self) -> Dict[str, Any]:
        return self.omit_none_values(
            {
                **super().api_data,
                "subject": self.subject,
                "text": self.text,
                "html": self.html,
                "category": self.category,
            }
        )
