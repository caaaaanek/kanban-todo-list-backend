from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.board import BoardRepository
from app.repositories.column import ColumnRepository
from app.schemas.column import ColumnCreate, ColumnOut
from app.services.board import BoardService
from app.services.column import ColumnService

router = APIRouter(prefix="/boards/{board_id}/columns", tags=["columns"])


def get_column_service(db: Session = Depends(get_db)) -> ColumnService:
    return ColumnService(ColumnRepository(db), BoardService(BoardRepository(db)))


def get_session_user_id(request: Request) -> int:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_id


@router.get("/", response_model=list[ColumnOut])
def list_columns(board_id: int, service: ColumnService = Depends(get_column_service), user_id: int = Depends(get_session_user_id)):
    return service.list_columns(board_id=board_id, user_id=user_id)


@router.post("/", response_model=ColumnOut, status_code=201)
def create_column(board_id: int, data: ColumnCreate, service: ColumnService = Depends(get_column_service), user_id: int = Depends(get_session_user_id)):
    return service.create_column(board_id=board_id, title=data.title, position=data.position, user_id=user_id)


@router.delete("/{column_id}", status_code=204)
def delete_column(board_id: int, column_id: int, service: ColumnService = Depends(get_column_service), user_id: int = Depends(get_session_user_id)):
    service.delete_column(column_id=column_id, board_id=board_id, user_id=user_id)
