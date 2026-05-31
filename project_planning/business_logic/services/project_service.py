from datetime import datetime
from typing import List, Optional, Dict

from business_logic.interfaces.i_project_service import IProjectService
from data_access.interfaces.i_project_repository import IProjectRepository
from data_access.interfaces.i_task_repository import ITaskRepository
from data_access.models.project_model import ProjectModel


class ProjectService(IProjectService):
    """
    Business logic for Projects.
    Depends on DAL interfaces only — concrete repositories are injected via DI.
    """

    def __init__(
        self,
        project_repo: IProjectRepository,
        task_repo: ITaskRepository,
    ) -> None:
        self._project_repo = project_repo
        self._task_repo = task_repo

    # ------------------------------------------------------------------ #

    def get_all_projects(self) -> List[ProjectModel]:
        return self._project_repo.get_all()

    def get_project(self, project_id: int) -> Optional[ProjectModel]:
        return self._project_repo.get_by_id(project_id)

    def create_project(self, name: str, start_date: str, end_date: str) -> ProjectModel:
        project = ProjectModel(
            name=name,
            start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
            end_date=datetime.strptime(end_date, "%Y-%m-%d").date(),
        )
        return self._project_repo.create(project)

    def update_project(
        self,
        project_id: int,
        name: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> Optional[ProjectModel]:
        project = self._project_repo.get_by_id(project_id)
        if not project:
            return None
        if name:
            project.name = name
        if start_date:
            project.start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        if end_date:
            project.end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        return self._project_repo.update(project)

    def delete_project(self, project_id: int) -> bool:
        return self._project_repo.delete(project_id)

    def calculate_progress(self, project_id: int) -> float:
        tasks = self._task_repo.get_by_project(project_id)
        if not tasks:
            return 0.0
        completed = sum(1 for t in tasks if t.status == "completed")
        return round(completed / len(tasks) * 100, 2)

    def validate_plan(self, project_id: int) -> Dict:
        project = self._project_repo.get_by_id(project_id)
        if not project:
            return {"valid": False, "errors": ["Project not found"]}

        tasks = self._task_repo.get_by_project(project_id)
        errors: List[str] = []

        if not tasks:
            errors.append("Project has no tasks.")

        unassigned = [t for t in tasks if not t.resources]
        if unassigned:
            errors.append(
                f"{len(unassigned)} task(s) have no assigned resources: "
                + ", ".join(str(t.id) for t in unassigned)
            )

        if project.end_date < project.start_date:
            errors.append("Project end_date is before start_date.")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "project_id": project_id,
            "total_tasks": len(tasks),
            "unassigned_tasks": len(unassigned),
        }
