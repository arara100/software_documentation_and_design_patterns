from abc import ABC, abstractmethod
from typing import Any


class IResourceController(ABC):
    """Presentation-layer interface for Resource endpoints. No logic implemented yet."""

    @abstractmethod
    def get_resources(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get_resource(self, resource_id: int) -> Any:
        raise NotImplementedError

    @abstractmethod
    def create_resource(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def update_resource(self, resource_id: int) -> Any:
        raise NotImplementedError

    @abstractmethod
    def delete_resource(self, resource_id: int) -> Any:
        raise NotImplementedError
