from abc import ABC, abstractmethod
from typing import List, Optional
from data_access.models.project_model import ProjectModel


class IProjectRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[ProjectModel]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, project_id: int) -> Optional[ProjectModel]:
        raise NotImplementedError

    @abstractmethod
    def create(self, project: ProjectModel) -> ProjectModel:
        raise NotImplementedError

    @abstractmethod
    def update(self, project: ProjectModel) -> ProjectModel:
        raise NotImplementedError

    @abstractmethod
    def delete(self, project_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def save_all(self, projects: List[ProjectModel]) -> List[ProjectModel]:
        raise NotImplementedError
