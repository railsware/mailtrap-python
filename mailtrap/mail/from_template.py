from typing import Any
from typing import Dict
from typing import List
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
        to: List[Address],
        template_uuid: str,
        template_variables: Optional[Dict[str, Any]] = None,
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
        self.template_uuid = template_uuid
        self.template_variables = template_variables

    @property
    def api_data(self) -> Dict[str, Any]:
        return self.omit_none_values(
            {
                **super().api_data,
                "template_uuid": self.template_uuid,
                "template_variables": self.template_variables,
            }
        )
