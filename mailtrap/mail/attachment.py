from enum import Enum
from typing import Any
from typing import Dict
from typing import Optional

from mailtrap.mail.base_entity import BaseEntity


class Disposition(Enum):
    INLINE = "inline"
    ATTACHMENT = "attachment"


class Attachment(BaseEntity):
    def __init__(
        self,
        content: bytes,
        filename: str,
        disposition: Optional[Disposition] = None,
        mimetype: Optional[str] = None,
        content_id: Optional[str] = None,
    ) -> None:
        self.content = content
        self.filename = filename
        self.mimetype = mimetype
        self.disposition = disposition
        self.content_id = content_id

    @property
    def api_data(self) -> Dict[str, Any]:
        return self.omit_none_values(
            {
                "content": self.content.decode(),
                "filename": self.filename,
                "type": self.mimetype,
                "disposition": self.disposition.value if self.disposition else None,
                "content_id": self.content_id,
            }
        )
