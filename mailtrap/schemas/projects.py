from pydantic import BaseModel
from mailtrap.schemas.inboxes import Inbox
from mailtrap.schemas.permissions import Permissions


class ShareLinks(BaseModel):
    admin: str
    viewer: str


class Project(BaseModel):
    id: int
    name: str
    share_links: ShareLinks
    inboxes: list[Inbox]
    permissions: Permissions
