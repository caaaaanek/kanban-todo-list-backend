from sqlalchemy.orm import Session

from app.models.column import Column


class ColumnRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_board(self, board_id: int) -> list[Column]:
        return self.db.query(Column).filter(Column.board_id == board_id).order_by(Column.position).all()

    def get_by_id(self, column_id: int) -> Column | None:
        return self.db.get(Column, column_id)

    def create(self, title: str, position: int, board_id: int) -> Column:
        column = Column(title=title, position=position, board_id=board_id)
        self.db.add(column)
        self.db.commit()
        self.db.refresh(column)
        return column

    def delete(self, column: Column) -> None:
        self.db.delete(column)
        self.db.commit()
