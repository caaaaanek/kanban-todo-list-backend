from pydantic import BaseModel


class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    position: int = 0


class TaskOut(BaseModel):
    id: int
    title: str
    description: str | None
    position: int
    column_id: int

    model_config = {"from_attributes": True}
