from dataclasses import dataclass

from mailtrap.models.base import BaseModel


@dataclass
class Permissions(BaseModel):
    can_read: bool
    can_update: bool
    can_destroy: bool
    can_leave: bool
