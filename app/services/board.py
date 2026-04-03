from fastapi import HTTPException

from app.models.board import Board
from app.repositories.board import BoardRepository


class BoardService:
    def __init__(self, repo: BoardRepository):
        self.repo = repo

    def list_boards(self, user_id: int) -> list[Board]:
        return self.repo.get_all_by_user(user_id)

    def create_board(self, title: str, user_id: int) -> Board:
        return self.repo.create(title=title, user_id=user_id)

    def get_board_for_user(self, board_id: int, user_id: int) -> Board:
        board = self.repo.get_by_id(board_id)
        if not board or board.user_id != user_id:
            raise HTTPException(status_code=404, detail="Board not found")
        return board

    def delete_board(self, board_id: int, user_id: int) -> None:
        board = self.get_board_for_user(board_id, user_id)
        self.repo.delete(board)
