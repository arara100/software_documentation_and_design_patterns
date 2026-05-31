from typing import List, Optional
from sqlalchemy.orm import Session
from data_access.interfaces.i_task_repository import ITaskRepository
from data_access.models.task_model import TaskModel
from data_access.models.resource_model import ResourceModel


class TaskRepository(ITaskRepository):

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_all(self) -> List[TaskModel]:
        return self._session.query(TaskModel).all()

    def get_by_id(self, task_id: int) -> Optional[TaskModel]:
        return self._session.query(TaskModel).filter(TaskModel.id == task_id).first()

    def get_by_project(self, project_id: int) -> List[TaskModel]:
        return (
            self._session.query(TaskModel)
            .filter(TaskModel.project_id == project_id)
            .all()
        )

    def create(self, task: TaskModel) -> TaskModel:
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)
        return task

    def update(self, task: TaskModel) -> TaskModel:
        merged = self._session.merge(task)
        self._session.commit()
        self._session.refresh(merged)
        return merged

    def delete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)
        if not task:
            return False
        self._session.delete(task)
        self._session.commit()
        return True

    def save_all(self, tasks: List[TaskModel]) -> List[TaskModel]:
        self._session.add_all(tasks)
        self._session.flush()
        self._session.commit()
        return tasks

    def assign_resource(self, task_id: int, resource_id: int) -> bool:
        task = self.get_by_id(task_id)
        resource = self._session.query(ResourceModel).filter(ResourceModel.id == resource_id).first()
        if not task or not resource:
            return False
        if resource not in task.resources:
            task.resources.append(resource)
            self._session.commit()
        return True

    def remove_resource(self, task_id: int, resource_id: int) -> bool:
        task = self.get_by_id(task_id)
        resource = self._session.query(ResourceModel).filter(ResourceModel.id == resource_id).first()
        if not task or not resource:
            return False
        if resource in task.resources:
            task.resources.remove(resource)
            self._session.commit()
        return True
