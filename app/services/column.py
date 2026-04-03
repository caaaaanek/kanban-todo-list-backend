from fastapi import HTTPException

from app.models.column import Column
from app.repositories.column import ColumnRepository
from app.services.board import BoardService


class ColumnService:
    def __init__(self, repo: ColumnRepository, board_service: BoardService):
        self.repo = repo
        self.board_service = board_service

    def list_columns(self, board_id: int, user_id: int) -> list[Column]:
        self.board_service.get_board_for_user(board_id, user_id)
        return self.repo.get_all_by_board(board_id)

    def create_column(self, board_id: int, title: str, position: int, user_id: int) -> Column:
        self.board_service.get_board_for_user(board_id, user_id)
        return self.repo.create(title=title, position=position, board_id=board_id)

    def get_column_for_board(self, column_id: int, board_id: int, user_id: int) -> Column:
        self.board_service.get_board_for_user(board_id, user_id)
        column = self.repo.get_by_id(column_id)
        if not column or column.board_id != board_id:
            raise HTTPException(status_code=404, detail="Column not found")
        return column

    def delete_column(self, column_id: int, board_id: int, user_id: int) -> None:
        column = self.get_column_for_board(column_id, board_id, user_id)
        self.repo.delete(column)
