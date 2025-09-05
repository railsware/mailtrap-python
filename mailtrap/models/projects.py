from typing import Optional

from pydantic.dataclasses import dataclass

from mailtrap.models.common import RequestParams
from mailtrap.models.inboxes import Inbox
from mailtrap.models.permissions import Permissions


@dataclass
class ShareLinks:
    admin: str
    viewer: str


@dataclass
class Project:
    id: int
    name: str
    inboxes: list[Inbox]
    permissions: Permissions
    share_links: Optional[ShareLinks] = None


@dataclass
class ProjectParams(RequestParams):
    name: str
