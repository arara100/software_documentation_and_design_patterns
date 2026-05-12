from abc import ABC, abstractmethod
from typing import List, Optional
from data_access.models.resource_model import ResourceModel


class IResourceRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[ResourceModel]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, resource_id: int) -> Optional[ResourceModel]:
        raise NotImplementedError

    @abstractmethod
    def create(self, resource: ResourceModel) -> ResourceModel:
        raise NotImplementedError

    @abstractmethod
    def update(self, resource: ResourceModel) -> ResourceModel:
        raise NotImplementedError

    @abstractmethod
    def delete(self, resource_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def save_all(self, resources: List[ResourceModel]) -> List[ResourceModel]:
        raise NotImplementedError
