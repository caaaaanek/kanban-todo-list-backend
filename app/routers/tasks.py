from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.board import Board
from app.models.column import Column
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskOut

router = APIRouter(prefix="/boards/{board_id}/columns/{column_id}/tasks", tags=["tasks"])


def get_current_user_id(request: Request) -> int:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_id


def get_column(board_id: int, column_id: int, user_id: int, db: Session) -> Column:
    board = db.query(Board).filter(Board.id == board_id, Board.user_id == user_id).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    column = db.query(Column).filter(Column.id == column_id, Column.board_id == board_id).first()
    if not column:
        raise HTTPException(status_code=404, detail="Column not found")
    return column


@router.get("/", response_model=list[TaskOut])
def list_tasks(board_id: int, column_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    get_column(board_id, column_id, user_id, db)
    return db.query(Task).filter(Task.column_id == column_id).order_by(Task.position).all()


@router.post("/", response_model=TaskOut, status_code=201)
def create_task(board_id: int, column_id: int, data: TaskCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    get_column(board_id, column_id, user_id, db)
    task = Task(title=data.title, description=data.description, position=data.position, column_id=column_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(board_id: int, column_id: int, task_id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)):
    get_column(board_id, column_id, user_id, db)
    task = db.query(Task).filter(Task.id == task_id, Task.column_id == column_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
