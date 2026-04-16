from infrastructure.database import get_session
from data_access.repositories.project_repository import ProjectRepository
from data_access.repositories.task_repository import TaskRepository
from data_access.repositories.resource_repository import ResourceRepository
from data_access.csv_reader import CsvReader
from business_logic.services.project_service import ProjectService
from business_logic.services.task_service import TaskService
from business_logic.services.resource_service import ResourceService
from business_logic.services.plan_service import PlanService


class DIContainer:
    """
    Dependency Injection container.
    Wires BLL services with DAL repositories via interfaces (IoC).
    All BLL services receive DAL interfaces — never concrete implementations directly.
    """

    def __init__(self):
        self._session = get_session()
        self._project_repo = ProjectRepository(self._session)
        self._task_repo = TaskRepository(self._session)
        self._resource_repo = ResourceRepository(self._session)
        self._csv_reader = CsvReader()

    # ------------------------------------------------------------------ #
    # Public factory methods return BLL service typed against interfaces  #
    # ------------------------------------------------------------------ #

    def get_project_service(self) -> ProjectService:
        return ProjectService(self._project_repo, self._task_repo)

    def get_task_service(self) -> TaskService:
        return TaskService(self._task_repo, self._project_repo, self._resource_repo)

    def get_resource_service(self) -> ResourceService:
        return ResourceService(self._resource_repo)

    def get_plan_service(self) -> PlanService:
        return PlanService(
            self._project_repo,
            self._task_repo,
            self._resource_repo,
            self._csv_reader,
        )
