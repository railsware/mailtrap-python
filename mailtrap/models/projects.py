from pydantic import BaseModel
from pydantic import Field

from mailtrap.models.inboxes import Inbox
from mailtrap.models.permissions import Permissions


class ShareLinks(BaseModel):
    admin: str
    viewer: str


class Project(BaseModel):
    id: int
    name: str
    share_links: ShareLinks
    inboxes: list[Inbox]
    permissions: Permissions
