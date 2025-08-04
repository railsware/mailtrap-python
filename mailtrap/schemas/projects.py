from pydantic import BaseModel
from pydantic import Field

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


class ProjectInput(BaseModel):
    name: str = Field(min_length=2, max_length=100)
