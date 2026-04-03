from fastapi import HTTPException

from app.models.task import Task
from app.repositories.task import TaskRepository
from app.services.column import ColumnService


class TaskService:
    def __init__(self, repo: TaskRepository, column_service: ColumnService):
        self.repo = repo
        self.column_service = column_service

    def list_tasks(self, column_id: int, board_id: int, user_id: int) -> list[Task]:
        self.column_service.get_column_for_board(column_id, board_id, user_id)
        return self.repo.get_all_by_column(column_id)

    def create_task(self, column_id: int, board_id: int, title: str, description: str | None, position: int, user_id: int) -> Task:
        self.column_service.get_column_for_board(column_id, board_id, user_id)
        return self.repo.create(title=title, description=description, position=position, column_id=column_id)

    def delete_task(self, task_id: int, column_id: int, board_id: int, user_id: int) -> None:
        self.column_service.get_column_for_board(column_id, board_id, user_id)
        task = self.repo.get_by_id(task_id)
        if not task or task.column_id != column_id:
            raise HTTPException(status_code=404, detail="Task not found")
        self.repo.delete(task)
