from abc import ABC, abstractmethod
from typing import List, Dict


class ICsvReader(ABC):

    @abstractmethod
    def read(self, file_path: str) -> List[Dict[str, str]]:
        """Read CSV file and return list of row dicts."""
        raise NotImplementedError
