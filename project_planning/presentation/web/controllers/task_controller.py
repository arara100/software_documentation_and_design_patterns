from flask import Blueprint, render_template, request, redirect, url_for, flash
from presentation.api.dependencies import get_container

tasks_bp = Blueprint("tasks", __name__, url_prefix="/tasks")

_STATUSES = ["pending", "in_progress", "completed", "on_hold"]
_TASK_TYPES = ["task", "milestone", "dependency"]
_DEP_TYPES = ["finish_to_start", "start_to_start", "finish_to_finish", "start_to_finish"]


# ── LIST ──────────────────────────────────────────────────────────────────────
@tasks_bp.route("/")
def index():
    svc = get_container().get_task_service()
    tasks = svc.get_all_tasks()
    return render_template("tasks/index.html", tasks=tasks)


# ── DETAIL ────────────────────────────────────────────────────────────────────
@tasks_bp.route("/<int:task_id>")
def detail(task_id: int):
    svc = get_container().get_task_service()
    task = svc.get_task(task_id)
    if not task:
        flash("Задачу не знайдено.", "danger")
        return redirect(url_for("tasks.index"))
    res_svc = get_container().get_resource_service()
    all_resources = res_svc.get_all_resources()
    assigned_ids = {r.id for r in task.resources}
    return render_template(
        "tasks/detail.html",
        task=task,
        all_resources=all_resources,
        assigned_ids=assigned_ids,
        statuses=_STATUSES,
    )


# ── CREATE ────────────────────────────────────────────────────────────────────
@tasks_bp.route("/create", methods=["GET", "POST"])
def create():
    proj_svc = get_container().get_project_service()
    projects = proj_svc.get_all_projects()
    if request.method == "POST":
        try:
            project_id = int(request.form["project_id"])
            name = request.form.get("name", "").strip()
            duration = int(request.form.get("duration", 1))
            status = request.form.get("status", "pending")
            task_type = request.form.get("task_type", "task")
            is_critical = request.form.get("is_critical") == "on"
            dependency_type = request.form.get("dependency_type") or None

            svc = get_container().get_task_service()
            svc.create_task(
                project_id=project_id,
                name=name,
                duration=duration,
                status=status,
                task_type=task_type,
                is_critical=is_critical if task_type == "milestone" else None,
                dependency_type=dependency_type if task_type == "dependency" else None,
            )
            flash(f"Задачу «{name}» успішно створено.", "success")
            return redirect(url_for("tasks.index"))
        except Exception as exc:
            flash(f"Помилка: {exc}", "danger")
    return render_template(
        "tasks/create.html",
        projects=projects,
        statuses=_STATUSES,
        task_types=_TASK_TYPES,
        dep_types=_DEP_TYPES,
    )


# ── EDIT ──────────────────────────────────────────────────────────────────────
@tasks_bp.route("/<int:task_id>/edit", methods=["GET", "POST"])
def edit(task_id: int):
    svc = get_container().get_task_service()
    task = svc.get_task(task_id)
    if not task:
        flash("Задачу не знайдено.", "danger")
        return redirect(url_for("tasks.index"))
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            duration = int(request.form.get("duration", task.duration))
            status = request.form.get("status", task.status)
            task_type = request.form.get("task_type", task.task_type)
            is_critical = request.form.get("is_critical") == "on"
            dependency_type = request.form.get("dependency_type") or None
            svc.update_task(
                task_id,
                name=name or None,
                duration=duration,
                status=status,
                task_type=task_type,
                is_critical=is_critical if task_type == "milestone" else None,
                dependency_type=dependency_type if task_type == "dependency" else None,
            )
            flash("Задачу оновлено.", "success")
            return redirect(url_for("tasks.detail", task_id=task_id))
        except Exception as exc:
            flash(f"Помилка: {exc}", "danger")
    return render_template(
        "tasks/edit.html",
        task=task,
        statuses=_STATUSES,
        task_types=_TASK_TYPES,
        dep_types=_DEP_TYPES,
    )


# ── DELETE ────────────────────────────────────────────────────────────────────
@tasks_bp.route("/<int:task_id>/delete", methods=["POST"])
def delete(task_id: int):
    svc = get_container().get_task_service()
    if svc.delete_task(task_id):
        flash("Задачу видалено.", "success")
    else:
        flash("Задачу не знайдено.", "danger")
    return redirect(url_for("tasks.index"))


# ── ASSIGN RESOURCE ───────────────────────────────────────────────────────────
@tasks_bp.route("/<int:task_id>/assign", methods=["POST"])
def assign_resource(task_id: int):
    resource_id = int(request.form["resource_id"])
    svc = get_container().get_task_service()
    try:
        svc.assign_resource(task_id, resource_id)
        flash("Ресурс призначено.", "success")
    except Exception as exc:
        flash(f"Помилка: {exc}", "danger")
    return redirect(url_for("tasks.detail", task_id=task_id))


# ── REMOVE RESOURCE ───────────────────────────────────────────────────────────
@tasks_bp.route("/<int:task_id>/resources/<int:resource_id>/remove", methods=["POST"])
def remove_resource(task_id: int, resource_id: int):
    svc = get_container().get_task_service()
    svc.remove_resource(task_id, resource_id)
    flash("Ресурс відкріплено.", "success")
    return redirect(url_for("tasks.detail", task_id=task_id))


# ── UPDATE STATUS ─────────────────────────────────────────────────────────────
@tasks_bp.route("/<int:task_id>/status", methods=["POST"])
def update_status(task_id: int):
    status = request.form.get("status", "")
    svc = get_container().get_task_service()
    try:
        svc.update_status(task_id, status)
        flash("Статус оновлено.", "success")
    except Exception as exc:
        flash(f"Помилка: {exc}", "danger")
    return redirect(url_for("tasks.detail", task_id=task_id))
