from sqlalchemy.orm import Session

from app.models.task import Task


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_column(self, column_id: int) -> list[Task]:
        return self.db.query(Task).filter(Task.column_id == column_id).order_by(Task.position).all()

    def get_by_id(self, task_id: int) -> Task | None:
        return self.db.get(Task, task_id)

    def create(self, title: str, description: str | None, position: int, column_id: int) -> Task:
        task = Task(title=title, description=description, position=position, column_id=column_id)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()
