from typing import Any
from typing import Optional

from pydantic import Field
from pydantic.dataclasses import dataclass

from mailtrap.models.mail.base import BaseMail


@dataclass
class MailFromTemplate(BaseMail):
    template_uuid: str = Field(...)  # type:ignore
    template_variables: Optional[dict[str, Any]] = None
