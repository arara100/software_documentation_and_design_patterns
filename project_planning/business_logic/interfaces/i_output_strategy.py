from abc import ABC, abstractmethod
from typing import Dict, Any, List


class IOutputStrategy(ABC):
    """
    Output Strategy Interface.
    
    Defines contract for different output implementations (Console, Kafka, File, etc).
    Allows decoupling of output logic from business logic.
    Enables switching output targets with zero code changes (config only).
    """

    @abstractmethod
    def output(self, message: str) -> None:
        """Output a single message."""
        pass

    @abstractmethod
    def output_dict(self, data: Dict[str, Any]) -> None:
        """Output a dictionary (e.g., import statistics)."""
        pass

    @abstractmethod
    def output_list(self, items: List[str]) -> None:
        """Output a list of items."""
        pass

    @abstractmethod
    def flush(self) -> None:
        """Ensure all data is sent/written (cleanup/finalize)."""
        pass
