from abc import ABCMeta
from collections.abc import Sequence
from typing import Any
from typing import Optional

from mailtrap.mail.address import Address
from mailtrap.mail.attachment import Attachment
from mailtrap.mail.base_entity import BaseEntity


class BaseMail(BaseEntity, metaclass=ABCMeta):
    """Base abstract class for mails."""

    def __init__(
        self,
        sender: Address,
        to: list[Address],
        cc: Optional[list[Address]] = None,
        bcc: Optional[list[Address]] = None,
        attachments: Optional[list[Attachment]] = None,
        headers: Optional[dict[str, str]] = None,
        custom_variables: Optional[dict[str, Any]] = None,
    ) -> None:
        self.sender = sender
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.attachments = attachments
        self.headers = headers
        self.custom_variables = custom_variables

    @property
    def api_data(self) -> dict[str, Any]:
        return self.omit_none_values(
            {
                "from": self.sender.api_data,
                "to": self.get_api_data_from_list(self.to),
                "cc": self.get_api_data_from_list(self.cc),
                "bcc": self.get_api_data_from_list(self.bcc),
                "attachments": self.get_api_data_from_list(self.attachments),
                "headers": self.headers,
                "custom_variables": self.custom_variables,
            }
        )

    @staticmethod
    def get_api_data_from_list(
        items: Optional[Sequence[BaseEntity]],
    ) -> Optional[list[dict[str, Any]]]:
        if items is None:
            return None

        return [item.api_data for item in items]
