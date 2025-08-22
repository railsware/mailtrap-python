from enum import Enum
from typing import Optional

from pydantic import Field
from pydantic import FieldSerializationInfo
from pydantic import field_serializer
from pydantic.dataclasses import dataclass

from mailtrap.models.common import RequestParams


class Disposition(str, Enum):
    INLINE = "inline"
    ATTACHMENT = "attachment"


@dataclass
class Attachment(RequestParams):
    content: bytes
    filename: str
    disposition: Optional[Disposition] = None
    mimetype: Optional[str] = Field(default=None, serialization_alias="type")
    content_id: Optional[str] = None

    @field_serializer("content")
    def serialize_content(self, value: bytes, _info: FieldSerializationInfo) -> str:
        return value.decode()
