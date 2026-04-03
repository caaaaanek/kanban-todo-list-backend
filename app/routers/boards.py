from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.board import Board
from app.schemas.board import BoardCreate, BoardOut

router = APIRouter(prefix="/boards", tags=["boards"])


def get_current_user_id(request: Request) -> int:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_id


@router.get("/", response_model=list[BoardOut])
def list_boards(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    return db.query(Board).filter(Board.user_id == user_id).all()


@router.post("/", response_model=BoardOut, status_code=201)
def create_board(data: BoardCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    board = Board(title=data.title, user_id=user_id)
    db.add(board)
    db.commit()
    db.refresh(board)
    return board


@router.delete("/{board_id}", status_code=204)
def delete_board(board_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    board = db.query(Board).filter(Board.id == board_id, Board.user_id == user_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    db.delete(board)
    db.commit()
