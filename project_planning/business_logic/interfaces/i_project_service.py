from abc import ABC, abstractmethod
from typing import List, Optional, Dict


class IProjectService(ABC):

    @abstractmethod
    def get_all_projects(self) -> List:
        raise NotImplementedError

    @abstractmethod
    def get_project(self, project_id: int) -> Optional[object]:
        raise NotImplementedError

    @abstractmethod
    def create_project(self, name: str, start_date: str, end_date: str) -> object:
        raise NotImplementedError

    @abstractmethod
    def update_project(
        self,
        project_id: int,
        name: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Optional[object]:
        raise NotImplementedError

    @abstractmethod
    def delete_project(self, project_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def calculate_progress(self, project_id: int) -> float:
        raise NotImplementedError

    @abstractmethod
    def validate_plan(self, project_id: int) -> Dict:
        raise NotImplementedError
