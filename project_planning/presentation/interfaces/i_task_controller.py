from abc import ABC, abstractmethod
from typing import Any


class ITaskController(ABC):
    """Presentation-layer interface for Task endpoints. No logic implemented yet."""

    @abstractmethod
    def get_tasks(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_task(self, task_id: int) -> Any:
        raise NotImplementedError

    @abstractmethod
    def create_task(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def update_task(self, task_id: int) -> Any:
        raise NotImplementedError

    @abstractmethod
    def delete_task(self, task_id: int) -> Any:
        raise NotImplementedError

    @abstractmethod
    def assign_resource(self, task_id: int) -> Any:
        raise NotImplementedError

    @abstractmethod
    def remove_resource(self, task_id: int, resource_id: int) -> Any:
        raise NotImplementedError

    @abstractmethod
    def update_status(self, task_id: int) -> Any:
        raise NotImplementedError
