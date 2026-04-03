from pydantic import BaseModel


class ColumnCreate(BaseModel):
    title: str
    position: int = 0


class ColumnOut(BaseModel):
    id: int
    title: str
    position: int
    board_id: int

    model_config = {"from_attributes": True}
