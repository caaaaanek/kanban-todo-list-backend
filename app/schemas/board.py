from pydantic import BaseModel


class BoardCreate(BaseModel):
    title: str


class BoardOut(BaseModel):
    id: int
    title: str
    user_id: int

    model_config = {"from_attributes": True}
