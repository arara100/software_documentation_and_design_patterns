from datetime import datetime
from typing import Dict, List, Optional

from business_logic.interfaces.i_plan_service import IPlanService
from business_logic.interfaces.i_output_strategy import IOutputStrategy
from data_access.interfaces.i_project_repository import IProjectRepository
from data_access.interfaces.i_task_repository import ITaskRepository
from data_access.interfaces.i_resource_repository import IResourceRepository
from data_access.interfaces.i_csv_reader import ICsvReader
from data_access.models.project_model import ProjectModel
from data_access.models.task_model import TaskModel
from data_access.models.resource_model import ResourceModel


class PlanService(IPlanService):
    """
    Orchestrates CSV import → model creation → DB persistence.
    Calls DAL interfaces only (IoC / DI).
    
    ЛР4: Використовує OutputStrategy для вводу розділеного від коду читання даних.
    Дозволяє вивід в консоль, Kafka, файл без змін в коді (тільки конфіг).
    """

    def __init__(
        self,
        project_repo: IProjectRepository,
        task_repo: ITaskRepository,
        resource_repo: IResourceRepository,
        csv_reader: ICsvReader,
        output_strategy: IOutputStrategy,
    ) -> None:
        self._project_repo = project_repo
        self._task_repo = task_repo
        self._resource_repo = resource_repo
        self._csv_reader = csv_reader
        self._output_strategy = output_strategy

    # ------------------------------------------------------------------ #

    def import_from_csv(self, file_path: str) -> Dict:
        """
        1. Read CSV via ICsvReader (DAL)
        2. Build model objects
        3. Persist via DAL repositories in the correct order
        4. Output statistics via OutputStrategy
        5. Return import statistics
        """
        rows: List[Dict] = self._csv_reader.read(file_path)
        self._output_strategy.output(f"📂 Читання CSV файлу: {file_path}")

        # --- Collect entities by csv-local ids ---
        projects: Dict[int, ProjectModel] = {}
        resources: Dict[int, ResourceModel] = {}
        tasks: Dict[int, TaskModel] = {}
        # (csv_task_id, csv_resource_id) pairs
        assignment_pairs: List[tuple] = []

        for row in rows:
            rt = row.get("record_type", "").strip().upper()

            if rt == "PROJECT":
                csv_id = int(row["id"])
                p = ProjectModel(
                    name=row["name"],
                    start_date=datetime.strptime(row["start_date"], "%Y-%m-%d").date(),
                    end_date=datetime.strptime(row["end_date"], "%Y-%m-%d").date(),
                )
                projects[csv_id] = p

            elif rt in ("TASK", "MILESTONE", "DEPENDENCY"):
                csv_id = int(row["id"])
                task_type = rt.lower()
                is_critical_raw = row.get("is_critical", "").strip().lower()
                t = TaskModel(
                    name=row["name"],
                    duration=int(row["duration"]),
                    status=row.get("status", "pending"),
                    task_type=task_type,
                    is_critical=(is_critical_raw == "true") if task_type == "milestone" else None,
                    dependency_type=row.get("dependency_type") or None if task_type == "dependency" else None,
                    project_id=int(row["project_id"]),  # temporary csv id, resolved below
                )
                tasks[csv_id] = (t, int(row["project_id"]))

            elif rt in ("HUMAN_RESOURCE", "MATERIAL_RESOURCE"):
                csv_id = int(row["id"])
                r_type = "human" if rt == "HUMAN_RESOURCE" else "material"
                r = ResourceModel(
                    name=row["name"],
                    resource_type=r_type,
                    role=row.get("role") or None if r_type == "human" else None,
                    skill_level=int(row["skill_level"]) if r_type == "human" and row.get("skill_level") else None,
                    quantity=int(row["quantity"]) if r_type == "material" and row.get("quantity") else None,
                )
                resources[csv_id] = r

            elif rt == "ASSIGNMENT":
                t_id = row.get("task_id", "").strip()
                r_id = row.get("resource_id", "").strip()
                if t_id and r_id:
                    assignment_pairs.append((int(t_id), int(r_id)))

        # --- Persist in correct FK order ---

        # 1. Save projects → get real DB ids
        project_objs = list(projects.values())
        self._project_repo.save_all(project_objs)
        csv_to_db_project = {csv_id: obj.id for csv_id, obj in projects.items()}

        # 2. Save resources → get real DB ids
        resource_objs = list(resources.values())
        self._resource_repo.save_all(resource_objs)
        csv_to_db_resource = {csv_id: obj.id for csv_id, obj in resources.items()}

        # 3. Fix project_id references in tasks and save
        task_objs = []
        csv_to_db_task: Dict[int, int] = {}
        for csv_task_id, (task_obj, csv_proj_id) in tasks.items():
            db_project_id = csv_to_db_project.get(csv_proj_id)
            if db_project_id is None:
                continue  # orphan task — skip
            task_obj.project_id = db_project_id
            task_objs.append(task_obj)

        self._task_repo.save_all(task_objs)
        for csv_task_id, (task_obj, _) in tasks.items():
            if task_obj.id:
                csv_to_db_task[csv_task_id] = task_obj.id

        # 4. Create assignments
        created_assignments = 0
        for csv_t_id, csv_r_id in assignment_pairs:
            db_t_id = csv_to_db_task.get(csv_t_id)
            db_r_id = csv_to_db_resource.get(csv_r_id)
            if db_t_id and db_r_id:
                self._task_repo.assign_resource(db_t_id, db_r_id)
                created_assignments += 1

        # --- Output statistics via strategy ---
        stats = {
            "projects": len(project_objs),
            "tasks": len(task_objs),
            "resources": len(resource_objs),
            "assignments": created_assignments,
        }
        self._output_strategy.output_dict(stats)
        self._output_strategy.flush()

        return stats

    def export_plan(self, project_id: int) -> Optional[Dict]:
        project = self._project_repo.get_by_id(project_id)
        if not project:
            return None

        tasks = self._task_repo.get_by_project(project_id)
        task_data = [
            {
                "id": t.id,
                "name": t.name,
                "duration": t.duration,
                "status": t.status,
                "task_type": t.task_type,
                "is_critical": t.is_critical,
                "dependency_type": t.dependency_type,
                "resources": [
                    {"id": r.id, "name": r.name, "type": r.resource_type}
                    for r in t.resources
                ],
            }
            for t in tasks
        ]

        result = {
            "project": {
                "id": project.id,
                "name": project.name,
                "start_date": str(project.start_date),
                "end_date": str(project.end_date),
            },
            "tasks": task_data,
            "total_tasks": len(tasks),
        }
        
        # --- Output via strategy ---
        self._output_strategy.output(f"📋 Експорт проекту: {project.name}")
        self._output_strategy.output_list([t["name"] for t in task_data])
        self._output_strategy.flush()
        
        return result
