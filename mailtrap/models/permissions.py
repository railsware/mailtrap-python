from pydantic.dataclasses import dataclass


@dataclass
class Permissions:
    can_read: bool
    can_update: bool
    can_destroy: bool
    can_leave: bool
