from abc import ABC, abstractmethod
from typing import Any


class IOutputStrategy(ABC):
    """Strategy interface for outputting data (console, Kafka, etc.)."""

    @abstractmethod
    def output(self, data: Any) -> None:
        """Send *data* to the configured destination."""
        raise NotImplementedError
