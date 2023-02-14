from abc import ABCMeta
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence

from mailtrap.mail.address import Address
from mailtrap.mail.attachment import Attachment
from mailtrap.mail.base_entity import BaseEntity


class BaseMail(BaseEntity, metaclass=ABCMeta):
    """Base abstract class for mails."""

    def __init__(
        self,
        sender: Address,
        to: List[Address],
        cc: Optional[List[Address]] = None,
        bcc: Optional[List[Address]] = None,
        attachments: Optional[List[Attachment]] = None,
        headers: Optional[Dict[str, str]] = None,
        custom_variables: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.sender = sender
        self.to = to
        self.cc = cc
        self.bcc = bcc
        self.attachments = attachments
        self.headers = headers
        self.custom_variables = custom_variables

    @property
    def api_data(self) -> Dict[str, Any]:
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
    ) -> Optional[List[Dict[str, Any]]]:
        if items is None:
            return None

        return [item.api_data for item in items]
