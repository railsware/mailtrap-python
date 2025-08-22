from typing import Optional

from pydantic.dataclasses import dataclass

from mailtrap.models.common import RequestParams


@dataclass
class CreateEmailTemplateParams(RequestParams):
    name: str
    subject: str
    category: str
    body_text: Optional[str] = None
    body_html: Optional[str] = None


@dataclass
class UpdateEmailTemplateParams(RequestParams):
    name: Optional[str] = None
    subject: Optional[str] = None
    category: Optional[str] = None
    body_text: Optional[str] = None
    body_html: Optional[str] = None

    def __post_init__(self) -> None:
        if all(
            value is None
            for value in [
                self.name,
                self.subject,
                self.category,
                self.body_text,
                self.body_html,
            ]
        ):
            raise ValueError("At least one field must be provided for update action")


@dataclass
class EmailTemplate:
    id: int
    name: str
    uuid: str
    category: str
    subject: str
    body_text: Optional[str]
    body_html: Optional[str]
    created_at: str
    updated_at: str
