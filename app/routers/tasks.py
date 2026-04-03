from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.board import BoardRepository
from app.repositories.column import ColumnRepository
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskOut
from app.services.board import BoardService
from app.services.column import ColumnService
from app.services.task import TaskService

router = APIRouter(prefix="/boards/{board_id}/columns/{column_id}/tasks", tags=["tasks"])


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    board_service = BoardService(BoardRepository(db))
    column_service = ColumnService(ColumnRepository(db), board_service)
    return TaskService(TaskRepository(db), column_service)


def get_session_user_id(request: Request) -> int:
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user_id


@router.get("/", response_model=list[TaskOut])
def list_tasks(board_id: int, column_id: int, service: TaskService = Depends(get_task_service), user_id: int = Depends(get_session_user_id)):
    return service.list_tasks(column_id=column_id, board_id=board_id, user_id=user_id)


@router.post("/", response_model=TaskOut, status_code=201)
def create_task(board_id: int, column_id: int, data: TaskCreate, service: TaskService = Depends(get_task_service), user_id: int = Depends(get_session_user_id)):
    return service.create_task(column_id=column_id, board_id=board_id, title=data.title, description=data.description, position=data.position, user_id=user_id)


@router.delete("/{task_id}", status_code=204)
def delete_task(board_id: int, column_id: int, task_id: int, service: TaskService = Depends(get_task_service), user_id: int = Depends(get_session_user_id)):
    service.delete_task(task_id=task_id, column_id=column_id, board_id=board_id, user_id=user_id)
