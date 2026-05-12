from abc import ABC, abstractmethod
from typing import List, Optional


class ITaskService(ABC):

    @abstractmethod
    def get_all_tasks(self) -> List:
        raise NotImplementedError

    @abstractmethod
    def get_task(self, task_id: int) -> Optional[object]:
        raise NotImplementedError

    @abstractmethod
    def get_tasks_by_project(self, project_id: int) -> List:
        raise NotImplementedError

    @abstractmethod
    def create_task(
        self,
        project_id: int,
        name: str,
        duration: int,
        status: str = "pending",
        task_type: str = "task",
        is_critical: Optional[bool] = None,
        dependency_type: Optional[str] = None,
    ) -> object:
        raise NotImplementedError

    @abstractmethod
    def update_task(self, task_id: int, **kwargs) -> Optional[object]:
        raise NotImplementedError

    @abstractmethod
    def delete_task(self, task_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def assign_resource(self, task_id: int, resource_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def remove_resource(self, task_id: int, resource_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update_status(self, task_id: int, status: str) -> Optional[object]:
        raise NotImplementedError
