from flask import Blueprint, render_template, request, redirect, url_for, flash
from presentation.api.dependencies import get_container

resources_bp = Blueprint("resources", __name__, url_prefix="/resources")

_RESOURCE_TYPES = ["human", "material"]
_ROLES = ["Developer", "Designer", "Manager", "Analyst", "Tester", "DevOps", "Architect"]


# ── LIST ──────────────────────────────────────────────────────────────────────
@resources_bp.route("/")
def index():
    svc = get_container().get_resource_service()
    resources = svc.get_all_resources()
    return render_template("resources/index.html", resources=resources)


# ── CREATE ────────────────────────────────────────────────────────────────────
@resources_bp.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            resource_type = request.form.get("resource_type", "human")
            svc = get_container().get_resource_service()
            if resource_type == "human":
                role = request.form.get("role", "").strip()
                skill_level = int(request.form.get("skill_level", 5))
                svc.create_human_resource(name=name, role=role, skill_level=skill_level)
            else:
                quantity = int(request.form.get("quantity", 1))
                svc.create_material_resource(name=name, quantity=quantity)
            flash(f"Ресурс «{name}» успішно створено.", "success")
            return redirect(url_for("resources.index"))
        except Exception as exc:
            flash(f"Помилка: {exc}", "danger")
    return render_template("resources/create.html", resource_types=_RESOURCE_TYPES, roles=_ROLES)


# ── EDIT ──────────────────────────────────────────────────────────────────────
@resources_bp.route("/<int:resource_id>/edit", methods=["GET", "POST"])
def edit(resource_id: int):
    svc = get_container().get_resource_service()
    resource = svc.get_resource(resource_id)
    if not resource:
        flash("Ресурс не знайдено.", "danger")
        return redirect(url_for("resources.index"))
    if request.method == "POST":
        try:
            name = request.form.get("name", "").strip()
            role = request.form.get("role", "").strip() or None
            skill_level_raw = request.form.get("skill_level", "")
            skill_level = int(skill_level_raw) if skill_level_raw else None
            quantity_raw = request.form.get("quantity", "")
            quantity = int(quantity_raw) if quantity_raw else None
            svc.update_resource(
                resource_id,
                name=name or None,
                role=role,
                skill_level=skill_level,
                quantity=quantity,
            )
            flash("Ресурс оновлено.", "success")
            return redirect(url_for("resources.index"))
        except Exception as exc:
            flash(f"Помилка: {exc}", "danger")
    return render_template("resources/edit.html", resource=resource, roles=_ROLES)


# ── DELETE ────────────────────────────────────────────────────────────────────
@resources_bp.route("/<int:resource_id>/delete", methods=["POST"])
def delete(resource_id: int):
    svc = get_container().get_resource_service()
    if svc.delete_resource(resource_id):
        flash("Ресурс видалено.", "success")
    else:
        flash("Ресурс не знайдено.", "danger")
    return redirect(url_for("resources.index"))
