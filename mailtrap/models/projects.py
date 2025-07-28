from typing import Any, List, Dict


class ShareLinks:
    def __init__(self, admin: str, viewer: str):
        self.admin = admin
        self.viewer = viewer


class Permissions:
    def __init__(
        self, 
        can_read: bool, 
        can_update: bool, 
        can_destroy: bool, 
        can_leave: bool
    ):
        self.can_read = can_read
        self.can_update = can_update
        self.can_destroy = can_destroy
        self.can_leave = can_leave


class Project:
    def __init__(
        self, 
        id: str, 
        name: str, 
        share_links: ShareLinks, 
        inboxes: List[Dict[str, Any]], 
        permissions: Permissions
    ):
        self.id = id
        self.name = name
        self.share_links = share_links
        self.inboxes = inboxes
        self.permissions = permissions

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Project":
        share_links = ShareLinks(**data["share_links"])
        permissions = Permissions(**data["permissions"])
        inboxes = data.get("inboxes", [])
        return cls(
            id=data["id"],
            name=data["name"],
            share_links=share_links,
            inboxes=inboxes,
            permissions=permissions,
        )
