from infrastructure.database import get_session
from infrastructure.config import Config
from data_access.repositories.project_repository import ProjectRepository
from data_access.repositories.task_repository import TaskRepository
from data_access.repositories.resource_repository import ResourceRepository
from data_access.csv_reader import CsvReader
from business_logic.services.project_service import ProjectService
from business_logic.services.task_service import TaskService
from business_logic.services.resource_service import ResourceService
from business_logic.services.plan_service import PlanService
from business_logic.interfaces.i_output_strategy import IOutputStrategy
from business_logic.strategies.console_output_strategy import ConsoleOutputStrategy
from business_logic.strategies.kafka_output_strategy import KafkaOutputStrategy
from business_logic.strategies.file_output_strategy import FileOutputStrategy
from business_logic.strategies.redis_output_strategy import RedisOutputStrategy
from business_logic.strategies.firebase_output_strategy import FirebaseOutputStrategy


class DIContainer:
    """
    Dependency Injection container.
    Wires BLL services with DAL repositories via interfaces (IoC).
    All BLL services receive DAL interfaces — never concrete implementations directly.
    
    ЛР4: Реалізація паттерну Strategy для виводу даних (OutputStrategy).
    Дозволяє переключення з консолі на Kafka/File/Redis/Firebase через конфіг без змін коду.
    """

    def __init__(self):
        self._session = get_session()
        self._project_repo = ProjectRepository(self._session)
        self._task_repo = TaskRepository(self._session)
        self._resource_repo = ResourceRepository(self._session)
        self._csv_reader = CsvReader()
        self._output_strategy = self._create_output_strategy()

    # ------------------------------------------------------------------ #
    # Output Strategy Factory (ЛР4)
    # ------------------------------------------------------------------ #

    def _create_output_strategy(self) -> IOutputStrategy:
        """
        Factory method to create the appropriate output strategy.
        Selection based on Config.OUTPUT_STRATEGY environment variable.
        
        Дозволені значення:
          - "console": вивід в консоль (за замовчуванням)
          - "kafka": вивід в Apache Kafka
          - "file": вивід в файл (JSONL)
          - "redis": вивід в Redis (pub/sub або list)
          - "firebase": вивід в Firebase Realtime Database
        """
        strategy_type = Config.OUTPUT_STRATEGY.lower()

        if strategy_type == "kafka":
            return KafkaOutputStrategy(
                bootstrap_servers=Config.KAFKA_BOOTSTRAP_SERVERS,
                topic=Config.KAFKA_TOPIC,
            )
        elif strategy_type == "file":
            return FileOutputStrategy(file_path=Config.OUTPUT_FILE_PATH)
        elif strategy_type == "redis":
            return RedisOutputStrategy(
                host=Config.REDIS_HOST,
                port=Config.REDIS_PORT,
                password=Config.REDIS_PASSWORD,
                db=Config.REDIS_DB,
                channel=Config.REDIS_CHANNEL,
                mode=Config.REDIS_MODE,
            )
        elif strategy_type == "firebase":
            return FirebaseOutputStrategy(
                credentials_path=Config.FIREBASE_CREDENTIALS_PATH,
                database_url=Config.FIREBASE_DATABASE_URL,
                db_path=Config.FIREBASE_DB_PATH,
            )
        else:  # "console" or any unknown value defaults to console
            return ConsoleOutputStrategy()

    def get_output_strategy(self) -> IOutputStrategy:
        """Get the configured output strategy."""
        return self._output_strategy

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
            self._output_strategy,
        )
