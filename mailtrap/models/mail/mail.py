from typing import Optional

from pydantic import Field
from pydantic.dataclasses import dataclass

from mailtrap.models.mail.base import BaseMail


@dataclass
class Mail(BaseMail):
    subject: str = Field(...)  # type:ignore
    text: Optional[str] = None
    html: Optional[str] = None
    category: Optional[str] = None
