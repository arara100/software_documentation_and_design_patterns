from flask_restx import Namespace, Resource, fields

from infrastructure.config import Config
from presentation.api.dependencies import get_container


ns_plan = Namespace("plan", description="Plan import / export / validation")

validation_result = ns_plan.model(
    "ValidationResult",
    {
        "valid": fields.Boolean,
        "project_id": fields.Integer,
        "total_tasks": fields.Integer,
        "unassigned_tasks": fields.Integer,
        "errors": fields.List(fields.String),
    },
)

import_result = ns_plan.model(
    "ImportResult",
    {
        "projects": fields.Integer,
        "tasks": fields.Integer,
        "resources": fields.Integer,
        "assignments": fields.Integer,
    },
)


@ns_plan.route("/import")
class PlanImport(Resource):
    @ns_plan.marshal_with(import_result)
    @ns_plan.response(400, "Import failed")
    def post(self):
        """
        Import data from a CSV file into the database.
        Reads the path configured in CSV_FILE_PATH env variable.
        """
        svc = get_container().get_plan_service()
        try:
            result = svc.import_from_csv(Config.CSV_FILE_PATH)
        except FileNotFoundError:
            ns_plan.abort(400, f"CSV file not found: {Config.CSV_FILE_PATH}")
        except Exception as exc:
            ns_plan.abort(400, str(exc))
        return result


@ns_plan.route("/<int:project_id>/export")
class PlanExport(Resource):
    @ns_plan.response(404, "Project not found")
    def get(self, project_id: int):
        """Export the full plan for a project as JSON."""
        svc = get_container().get_plan_service()
        result = svc.export_plan(project_id)
        if not result:
            ns_plan.abort(404, "Project not found")
        return result


@ns_plan.route("/<int:project_id>/validate")
class PlanValidate(Resource):
    @ns_plan.marshal_with(validation_result)
    def get(self, project_id: int):
        """Validate plan: check for unassigned tasks and date consistency."""
        svc = get_container().get_project_service()
        return svc.validate_plan(project_id)
