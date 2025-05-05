from typing import Any
from typing import Optional

from mailtrap.mail.address import Address
from mailtrap.mail.attachment import Attachment
from mailtrap.mail.base import BaseMail


class MailFromTemplate(BaseMail):
    """Creates `EmailFromTemplate` request body for /api/send Mailtrap API v2
    endpoint."""

    def __init__(
        self,
        sender: Address,
        to: list[Address],
        template_uuid: str,
        template_variables: Optional[dict[str, Any]] = None,
        cc: Optional[list[Address]] = None,
        bcc: Optional[list[Address]] = None,
        attachments: Optional[list[Attachment]] = None,
        headers: Optional[dict[str, str]] = None,
        custom_variables: Optional[dict[str, Any]] = None,
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
        self.template_uuid = template_uuid
        self.template_variables = template_variables

    @property
    def api_data(self) -> dict[str, Any]:
        return self.omit_none_values(
            {
                **super().api_data,
                "template_uuid": self.template_uuid,
                "template_variables": self.template_variables,
            }
        )
