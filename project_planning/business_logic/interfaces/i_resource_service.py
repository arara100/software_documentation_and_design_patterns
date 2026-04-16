from abc import ABC, abstractmethod
from typing import List, Optional


class IResourceService(ABC):

    @abstractmethod
    def get_all_resources(self) -> List:
        raise NotImplementedError

    @abstractmethod
    def get_resource(self, resource_id: int) -> Optional[object]:
        raise NotImplementedError

    @abstractmethod
    def create_human_resource(
        self, name: str, role: str, skill_level: int
    ) -> object:
        raise NotImplementedError

    @abstractmethod
    def create_material_resource(
        self, name: str, quantity: int
    ) -> object:
        raise NotImplementedError

    @abstractmethod
    def update_resource(self, resource_id: int, **kwargs) -> Optional[object]:
        raise NotImplementedError

    @abstractmethod
    def delete_resource(self, resource_id: int) -> bool:
        raise NotImplementedError
