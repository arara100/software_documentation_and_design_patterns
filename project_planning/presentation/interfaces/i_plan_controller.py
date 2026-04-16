from abc import ABC, abstractmethod
from typing import Any


class IPlanController(ABC):
    """Presentation-layer interface for Plan endpoints. No logic implemented yet."""

    @abstractmethod
    def import_csv(self) -> Any:
        raise NotImplementedError

    @abstractmethod
    def export_plan(self, project_id: int) -> Any:
        raise NotImplementedError
