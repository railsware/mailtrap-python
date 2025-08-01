from dataclasses import dataclass

from mailtrap.models.base import BaseModel
from mailtrap.models.inboxes import Inbox
from mailtrap.models.permissions import Permissions


@dataclass
class ShareLinks(BaseModel):
    admin: str
    viewer: str


@dataclass
class Project(BaseModel):
    id: str
    name: str
    share_links: ShareLinks
    inboxes: list[Inbox]
    permissions: Permissions
