from flask import Blueprint, render_template, request, redirect, url_for, flash
from presentation.api.dependencies import get_container

projects_bp = Blueprint("projects", __name__, url_prefix="/projects")


# ── LIST ─────────────────────────────────────────────────────────────────────
@projects_bp.route("/")
def index():
    svc = get_container().get_project_service()
    projects = svc.get_all_projects()
    progress = {p.id: svc.calculate_progress(p.id) for p in projects}
    return render_template("projects/index.html", projects=projects, progress=progress)


# ── DETAIL ────────────────────────────────────────────────────────────────────
@projects_bp.route("/<int:project_id>")
def detail(project_id: int):
    svc = get_container().get_project_service()
    task_svc = get_container().get_task_service()
    project = svc.get_project(project_id)
    if not project:
        flash("Проект не знайдено.", "danger")
        return redirect(url_for("projects.index"))
    tasks = task_svc.get_tasks_by_project(project_id)
    progress = svc.calculate_progress(project_id)
    validation = svc.validate_plan(project_id)
    return render_template(
        "projects/detail.html",
        project=project,
        tasks=tasks,
        progress=progress,
        validation=validation,
    )


# ── CREATE ────────────────────────────────────────────────────────────────────
@projects_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        start_date = request.form.get("start_date", "").strip()
        end_date = request.form.get("end_date", "").strip()
        if not name or not start_date or not end_date:
            flash("Усі поля обов'язкові.", "warning")
            return render_template("projects/create.html")
        try:
            svc = get_container().get_project_service()
            svc.create_project(name, start_date, end_date)
            flash(f"Проект «{name}» успішно створено.", "success")
            return redirect(url_for("projects.index"))
        except Exception as exc:
            flash(f"Помилка: {exc}", "danger")
    return render_template("projects/create.html")


# ── EDIT ──────────────────────────────────────────────────────────────────────
@projects_bp.route("/<int:project_id>/edit", methods=["GET", "POST"])
def edit(project_id: int):
    svc = get_container().get_project_service()
    project = svc.get_project(project_id)
    if not project:
        flash("Проект не знайдено.", "danger")
        return redirect(url_for("projects.index"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        start_date = request.form.get("start_date", "").strip()
        end_date = request.form.get("end_date", "").strip()
        try:
            svc.update_project(
                project_id,
                name=name or None,
                start_date=start_date or None,
                end_date=end_date or None,
            )
            flash("Проект оновлено.", "success")
            return redirect(url_for("projects.detail", project_id=project_id))
        except Exception as exc:
            flash(f"Помилка: {exc}", "danger")
    return render_template("projects/edit.html", project=project)


# ── DELETE ────────────────────────────────────────────────────────────────────
@projects_bp.route("/<int:project_id>/delete", methods=["POST"])
def delete(project_id: int):
    svc = get_container().get_project_service()
    if svc.delete_project(project_id):
        flash("Проект видалено.", "success")
    else:
        flash("Проект не знайдено.", "danger")
    return redirect(url_for("projects.index"))
