
from dataclasses import dataclass
from mailtrap.models.base import BaseModel
from mailtrap.models.permissions import Permissions


@dataclass
class Inbox(BaseModel):
    id: int
    name: str
    username: str
    max_size: int
    status: str
    email_username: str
    email_username_enabled: bool
    sent_messages_count: int
    forwarded_messages_count: int
    used: bool
    forward_from_email_address: str
    project_id: int
    domain: str
    pop3_domain: str
    email_domain: str
    emails_count: int
    emails_unread_count: int
    smtp_ports: list[int]
    pop3_ports: list[int]
    max_message_size: int
    permissions: Permissions
    password: str | None = None  # Password is only available if you have admin permissions for the inbox.
    last_message_sent_at: str | None = None
