from typing import Any
from typing import Optional

from mailtrap.mail.base_entity import BaseEntity


class EmailTemplate(BaseEntity):
    def __init__(
        self,
        name: str,
        subject: str,
        category: str,
        body_html: Optional[str] = None,
        body_text: Optional[str] = None,
    ) -> None:
        self.name = name
        self.subject = subject
        self.category = category
        self.body_html = body_html
        self.body_text = body_text

    @property
    def api_data(self) -> dict[str, Any]:
        return self.omit_none_values(
            {
                "name": self.name,
                "subject": self.subject,
                "category": self.category,
                "body_html": self.body_html,
                "body_text": self.body_text,
            }
        )
