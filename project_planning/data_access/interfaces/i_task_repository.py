from abc import ABC, abstractmethod
from typing import List, Optional
from data_access.models.task_model import TaskModel


class ITaskRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[TaskModel]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[TaskModel]:
        raise NotImplementedError

    @abstractmethod
    def get_by_project(self, project_id: int) -> List[TaskModel]:
        raise NotImplementedError

    @abstractmethod
    def create(self, task: TaskModel) -> TaskModel:
        raise NotImplementedError

    @abstractmethod
    def update(self, task: TaskModel) -> TaskModel:
        raise NotImplementedError

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def save_all(self, tasks: List[TaskModel]) -> List[TaskModel]:
        raise NotImplementedError

    @abstractmethod
    def assign_resource(self, task_id: int, resource_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def remove_resource(self, task_id: int, resource_id: int) -> bool:
        raise NotImplementedError
