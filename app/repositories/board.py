from sqlalchemy.orm import Session

from app.models.board import Board


class BoardRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_user(self, user_id: int) -> list[Board]:
        return self.db.query(Board).filter(Board.user_id == user_id).all()

    def get_by_id(self, board_id: int) -> Board | None:
        return self.db.get(Board, board_id)

    def create(self, title: str, user_id: int) -> Board:
        board = Board(title=title, user_id=user_id)
        self.db.add(board)
        self.db.commit()
        self.db.refresh(board)
        return board

    def delete(self, board: Board) -> None:
        self.db.delete(board)
        self.db.commit()
