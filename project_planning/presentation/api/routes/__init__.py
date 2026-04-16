from flask_restx import Api

from presentation.api.routes.projects import ns_projects
from presentation.api.routes.tasks import ns_tasks
from presentation.api.routes.resources import ns_resources
from presentation.api.routes.plan import ns_plan


def register_namespaces(api: Api) -> None:
    api.add_namespace(ns_projects)
    api.add_namespace(ns_tasks)
    api.add_namespace(ns_resources)
    api.add_namespace(ns_plan)
