from presentation.web.controllers.project_controller import projects_bp
from presentation.web.controllers.task_controller import tasks_bp
from presentation.web.controllers.resource_controller import resources_bp


def register_blueprints(app):
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(resources_bp)
