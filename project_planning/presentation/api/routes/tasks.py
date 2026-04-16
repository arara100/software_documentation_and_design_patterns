from flask import request
from flask_restx import Namespace, Resource, fields

from presentation.api.dependencies import get_container
from presentation.api.serializers import task_to_dict


ns_tasks = Namespace("tasks", description="Task operations")

task_input = ns_tasks.model(
    "TaskInput",
    {
        "project_id": fields.Integer(required=True),
        "name": fields.String(required=True, example="Design DB schema"),
        "duration": fields.Integer(required=True, example=5),
        "status": fields.String(example="pending", default="pending"),
        "task_type": fields.String(
            example="task",
            description="task | milestone | dependency",
            default="task",
        ),
        "is_critical": fields.Boolean(description="Only for milestone type"),
        "dependency_type": fields.String(
            description="Only for dependency type",
            example="finish_to_start",
        ),
    },
)

task_output = ns_tasks.model(
    "Task",
    {
        "id": fields.Integer(readonly=True),
        "project_id": fields.Integer,
        "name": fields.String,
        "duration": fields.Integer,
        "status": fields.String,
        "task_type": fields.String,
        "is_critical": fields.Boolean,
        "dependency_type": fields.String,
        "resource_ids": fields.List(fields.Integer),
    },
)

status_input = ns_tasks.model(
    "StatusInput",
    {"status": fields.String(required=True, example="in_progress")},
)

assign_input = ns_tasks.model(
    "AssignInput",
    {"resource_id": fields.Integer(required=True)},
)


@ns_tasks.route("/")
class TaskList(Resource):
    @ns_tasks.marshal_list_with(task_output)
    def get(self):
        """List all tasks."""
        svc = get_container().get_task_service()
        return [task_to_dict(t) for t in svc.get_all_tasks()]

    @ns_tasks.expect(task_input, validate=True)
    @ns_tasks.marshal_with(task_output, code=201)
    def post(self):
        """Create a new task."""
        svc = get_container().get_task_service()
        data = request.json
        try:
            task = svc.create_task(
                project_id=data["project_id"],
                name=data["name"],
                duration=data["duration"],
                status=data.get("status", "pending"),
                task_type=data.get("task_type", "task"),
                is_critical=data.get("is_critical"),
                dependency_type=data.get("dependency_type"),
            )
        except ValueError as exc:
            ns_tasks.abort(400, str(exc))
        return task_to_dict(task), 201


@ns_tasks.route("/<int:task_id>")
class TaskItem(Resource):
    @ns_tasks.marshal_with(task_output)
    @ns_tasks.response(404, "Not found")
    def get(self, task_id: int):
        """Get a task by ID."""
        svc = get_container().get_task_service()
        task = svc.get_task(task_id)
        if not task:
            ns_tasks.abort(404, "Task not found")
        return task_to_dict(task)

    @ns_tasks.expect(task_input)
    @ns_tasks.marshal_with(task_output)
    @ns_tasks.response(404, "Not found")
    def put(self, task_id: int):
        """Update a task."""
        svc = get_container().get_task_service()
        data = request.json or {}
        allowed = {"name", "duration", "status", "task_type", "is_critical", "dependency_type"}
        kwargs = {k: v for k, v in data.items() if k in allowed}
        task = svc.update_task(task_id, **kwargs)
        if not task:
            ns_tasks.abort(404, "Task not found")
        return task_to_dict(task)

    @ns_tasks.response(204, "Deleted")
    @ns_tasks.response(404, "Not found")
    def delete(self, task_id: int):
        """Delete a task."""
        svc = get_container().get_task_service()
        if not svc.delete_task(task_id):
            ns_tasks.abort(404, "Task not found")
        return "", 204


@ns_tasks.route("/<int:task_id>/status")
class TaskStatus(Resource):
    @ns_tasks.expect(status_input, validate=True)
    @ns_tasks.marshal_with(task_output)
    def patch(self, task_id: int):
        """Update task status (pending | in_progress | completed | on_hold)."""
        svc = get_container().get_task_service()
        data = request.json
        try:
            task = svc.update_status(task_id, data["status"])
        except ValueError as exc:
            ns_tasks.abort(400, str(exc))
        if not task:
            ns_tasks.abort(404, "Task not found")
        return task_to_dict(task)


@ns_tasks.route("/<int:task_id>/resources")
class TaskResourceAssign(Resource):
    @ns_tasks.expect(assign_input, validate=True)
    @ns_tasks.response(200, "Resource assigned")
    @ns_tasks.response(400, "Bad request")
    def post(self, task_id: int):
        """Assign a resource to a task."""
        svc = get_container().get_task_service()
        resource_id = request.json["resource_id"]
        try:
            ok = svc.assign_resource(task_id, resource_id)
        except ValueError as exc:
            ns_tasks.abort(400, str(exc))
        if not ok:
            ns_tasks.abort(404, "Task or resource not found")
        return {"message": "Resource assigned successfully"}


@ns_tasks.route("/<int:task_id>/resources/<int:resource_id>")
class TaskResourceRemove(Resource):
    @ns_tasks.response(200, "Resource removed")
    @ns_tasks.response(404, "Not found")
    def delete(self, task_id: int, resource_id: int):
        """Remove a resource assignment from a task."""
        svc = get_container().get_task_service()
        ok = svc.remove_resource(task_id, resource_id)
        if not ok:
            ns_tasks.abort(404, "Task or resource not found")
        return {"message": "Resource removed successfully"}
