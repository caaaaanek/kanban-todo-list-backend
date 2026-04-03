from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.board import Board
from app.models.column import Column
from app.schemas.column import ColumnCreate, ColumnOut

router = APIRouter(prefix="/boards/{board_id}/columns", tags=["columns"])


def get_current_user_id(request: Request) -> int:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_id


def get_board(board_id: int, user_id: int, db: Session) -> Board:
    board = db.query(Board).filter(Board.id == board_id, Board.user_id == user_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board


@router.get("/", response_model=list[ColumnOut])
def list_columns(board_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    get_board(board_id, user_id, db)
    return db.query(Column).filter(Column.board_id == board_id).order_by(Column.position).all()


@router.post("/", response_model=ColumnOut, status_code=201)
def create_column(board_id: int, data: ColumnCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    get_board(board_id, user_id, db)
    column = Column(title=data.title, position=data.position, board_id=board_id)
    db.add(column)
    db.commit()
    db.refresh(column)
    return column


@router.delete("/{column_id}", status_code=204)
def delete_column(board_id: int, column_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    get_board(board_id, user_id, db)
    column = db.query(Column).filter(Column.id == column_id, Column.board_id == board_id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    db.delete(column)
    db.commit()
