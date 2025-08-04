from pydantic import BaseModel


class Permissions(BaseModel):
    can_read: bool
    can_update: bool
    can_destroy: bool
    can_leave: bool
