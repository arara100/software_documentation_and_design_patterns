from abc import ABC, abstractmethod
from typing import Any


class IProjectController(ABC):
    """Presentation-layer interface for Project endpoints. No logic implemented yet."""

    @abstractmethod
    def get_projects(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_project(self, project_id: int) -> Any:
        raise NotImplementedError

    @abstractmethod
    def create_project(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def update_project(self, project_id: int) -> Any:
        raise NotImplementedError

    @abstractmethod
    def delete_project(self, project_id: int) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_progress(self, project_id: int) -> Any:
        raise NotImplementedError

    @abstractmethod
    def validate_plan(self, project_id: int) -> Any:
        raise NotImplementedError
