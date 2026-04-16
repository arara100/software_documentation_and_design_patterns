from typing import List, Optional

from business_logic.interfaces.i_task_service import ITaskService
from data_access.interfaces.i_task_repository import ITaskRepository
from data_access.interfaces.i_project_repository import IProjectRepository
from data_access.interfaces.i_resource_repository import IResourceRepository
from data_access.models.task_model import TaskModel


class TaskService(ITaskService):
    """
    Business logic for Tasks.
    Depends on DAL interfaces only — concrete repositories are injected via DI.
    """

    def __init__(
        self,
        task_repo: ITaskRepository,
        project_repo: IProjectRepository,
        resource_repo: IResourceRepository,
    ) -> None:
        self._task_repo = task_repo
        self._project_repo = project_repo
        self._resource_repo = resource_repo

    # ------------------------------------------------------------------ #

    def get_all_tasks(self) -> List[TaskModel]:
        return self._task_repo.get_all()

    def get_task(self, task_id: int) -> Optional[TaskModel]:
        return self._task_repo.get_by_id(task_id)

    def get_tasks_by_project(self, project_id: int) -> List[TaskModel]:
        return self._task_repo.get_by_project(project_id)

    def create_task(
        self,
        project_id: int,
        name: str,
        duration: int,
        status: str = "pending",
        task_type: str = "task",
        is_critical: Optional[bool] = None,
        dependency_type: Optional[str] = None,
    ) -> TaskModel:
        if not self._project_repo.get_by_id(project_id):
            raise ValueError(f"Project {project_id} does not exist.")
        task = TaskModel(
            name=name,
            duration=duration,
            status=status,
            task_type=task_type,
            is_critical=is_critical,
            dependency_type=dependency_type,
            project_id=project_id,
        )
        return self._task_repo.create(task)

    def update_task(self, task_id: int, **kwargs) -> Optional[TaskModel]:
        task = self._task_repo.get_by_id(task_id)
        if not task:
            return None
        allowed = {"name", "duration", "status", "task_type", "is_critical", "dependency_type"}
        for key, value in kwargs.items():
            if key in allowed:
                setattr(task, key, value)
        return self._task_repo.update(task)

    def delete_task(self, task_id: int) -> bool:
        return self._task_repo.delete(task_id)

    def assign_resource(self, task_id: int, resource_id: int) -> bool:
        if not self._resource_repo.get_by_id(resource_id):
            raise ValueError(f"Resource {resource_id} does not exist.")
        return self._task_repo.assign_resource(task_id, resource_id)

    def remove_resource(self, task_id: int, resource_id: int) -> bool:
        return self._task_repo.remove_resource(task_id, resource_id)

    def update_status(self, task_id: int, status: str) -> Optional[TaskModel]:
        allowed_statuses = {"pending", "in_progress", "completed", "on_hold"}
        if status not in allowed_statuses:
            raise ValueError(f"Invalid status '{status}'. Allowed: {allowed_statuses}")
        return self.update_task(task_id, status=status)
