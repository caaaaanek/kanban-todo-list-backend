from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.board import BoardRepository
from app.schemas.board import BoardCreate, BoardOut
from app.services.board import BoardService

router = APIRouter(prefix="/boards", tags=["boards"])


def get_board_service(db: Session = Depends(get_db)) -> BoardService:
    return BoardService(BoardRepository(db))


def get_session_user_id(request: Request) -> int:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_id


@router.get("/", response_model=list[BoardOut])
def list_boards(service: BoardService = Depends(get_board_service), user_id: int = Depends(get_session_user_id)):
    return service.list_boards(user_id)


@router.post("/", response_model=BoardOut, status_code=201)
def create_board(data: BoardCreate, service: BoardService = Depends(get_board_service), user_id: int = Depends(get_session_user_id)):
    return service.create_board(title=data.title, user_id=user_id)


@router.delete("/{board_id}", status_code=204)
def delete_board(board_id: int, service: BoardService = Depends(get_board_service), user_id: int = Depends(get_session_user_id)):
    service.delete_board(board_id=board_id, user_id=user_id)
