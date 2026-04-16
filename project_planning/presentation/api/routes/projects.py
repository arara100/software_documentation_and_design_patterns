from flask import request
from flask_restx import Namespace, Resource, fields

from presentation.api.dependencies import get_container
from presentation.api.serializers import project_to_dict, task_to_dict


ns_projects = Namespace("projects", description="Project operations")

project_input = ns_projects.model(
    "ProjectInput",
    {
        "name": fields.String(required=True, example="E-Commerce Platform"),
        "start_date": fields.String(required=True, example="2024-01-01"),
        "end_date": fields.String(required=True, example="2024-12-31"),
    },
)

project_output = ns_projects.model(
    "Project",
    {
        "id": fields.Integer(readonly=True),
        "name": fields.String,
        "start_date": fields.String,
        "end_date": fields.String,
    },
)

task_output = ns_projects.model(
    "ProjectTask",
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


@ns_projects.route("/")
class ProjectList(Resource):
    @ns_projects.marshal_list_with(project_output)
    def get(self):
        """List all projects."""
        svc = get_container().get_project_service()
        return [project_to_dict(p) for p in svc.get_all_projects()]

    @ns_projects.expect(project_input, validate=True)
    @ns_projects.marshal_with(project_output, code=201)
    def post(self):
        """Create a new project."""
        svc = get_container().get_project_service()
        data = request.json
        project = svc.create_project(data["name"], data["start_date"], data["end_date"])
        return project_to_dict(project), 201


@ns_projects.route("/<int:project_id>")
class ProjectItem(Resource):
    @ns_projects.marshal_with(project_output)
    @ns_projects.response(404, "Not found")
    def get(self, project_id: int):
        """Get a project by ID."""
        svc = get_container().get_project_service()
        project = svc.get_project(project_id)
        if not project:
            ns_projects.abort(404, "Project not found")
        return project_to_dict(project)

    @ns_projects.expect(project_input)
    @ns_projects.marshal_with(project_output)
    @ns_projects.response(404, "Not found")
    def put(self, project_id: int):
        """Update a project."""
        svc = get_container().get_project_service()
        data = request.json or {}
        project = svc.update_project(project_id, **data)
        if not project:
            ns_projects.abort(404, "Project not found")
        return project_to_dict(project)

    @ns_projects.response(204, "Deleted")
    @ns_projects.response(404, "Not found")
    def delete(self, project_id: int):
        """Delete a project."""
        svc = get_container().get_project_service()
        if not svc.delete_project(project_id):
            ns_projects.abort(404, "Project not found")
        return "", 204


@ns_projects.route("/<int:project_id>/progress")
class ProjectProgress(Resource):
    def get(self, project_id: int):
        """Calculate project completion progress (%)."""
        svc = get_container().get_project_service()
        if not svc.get_project(project_id):
            ns_projects.abort(404, "Project not found")
        return {"project_id": project_id, "progress_percent": svc.calculate_progress(project_id)}


@ns_projects.route("/<int:project_id>/tasks")
class ProjectTasks(Resource):
    @ns_projects.marshal_list_with(task_output)
    def get(self, project_id: int):
        """List all tasks for a project."""
        svc = get_container().get_task_service()
        return [task_to_dict(t) for t in svc.get_tasks_by_project(project_id)]
