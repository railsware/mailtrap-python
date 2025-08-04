from pydantic import BaseModel


class DeletedObject(BaseModel):
    id: int
