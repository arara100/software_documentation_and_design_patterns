from abc import ABC, abstractmethod
from typing import Dict, Optional


class IPlanService(ABC):

    @abstractmethod
    def import_from_csv(self, file_path: str) -> Dict:
        """
        Read CSV, build models and persist them to the database.
        Returns statistics dict: {projects, tasks, resources, assignments}.
        """
        raise NotImplementedError

    @abstractmethod
    def export_plan(self, project_id: int) -> Optional[Dict]:
        """Return full plan as a serialisable dict."""
        raise NotImplementedError
