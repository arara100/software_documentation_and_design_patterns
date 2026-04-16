def project_to_dict(project) -> dict:
    return {
        "id": project.id,
        "name": project.name,
        "start_date": str(project.start_date),
        "end_date": str(project.end_date),
    }


def task_to_dict(task) -> dict:
    return {
        "id": task.id,
        "project_id": task.project_id,
        "name": task.name,
        "duration": task.duration,
        "status": task.status,
        "task_type": task.task_type,
        "is_critical": task.is_critical,
        "dependency_type": task.dependency_type,
        "resource_ids": [r.id for r in task.resources],
    }


def resource_to_dict(resource) -> dict:
    return {
        "id": resource.id,
        "name": resource.name,
        "resource_type": resource.resource_type,
        "role": resource.role,
        "skill_level": resource.skill_level,
        "quantity": resource.quantity,
    }
