#!/usr/bin/env python3
"""
CSV Data Generator for Project Planning System.

Generates a single multi-entity CSV file (>= 1000 rows) used by PlanService.import_from_csv().

Record types written:
  PROJECT          — project master record
  TASK             — regular task
  MILESTONE        — milestone task (is_critical field used)
  DEPENDENCY       — dependency task (dependency_type field used)
  HUMAN_RESOURCE   — human resource (role, skill_level)
  MATERIAL_RESOURCE— material resource (quantity)
  ASSIGNMENT       — many-to-many link between task and resource

Usage:
    python scripts/generate_csv.py                        # writes data/data.csv (default)
    python scripts/generate_csv.py --output my_data.csv   # custom path
    python scripts/generate_csv.py --projects 60 --resources 250
"""

import argparse
import csv
import os
import random
from datetime import date, timedelta

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

PROJECT_PREFIXES = [
    "E-Commerce Platform",
    "Mobile App",
    "Data Analytics",
    "Cloud Migration",
    "ERP Integration",
    "Security Audit",
    "API Gateway",
    "ML Pipeline",
    "DevOps Automation",
    "CRM System",
    "IoT Dashboard",
    "Payment Gateway",
    "HR Portal",
    "Supply Chain",
    "BI Reporting",
]

TASK_VERBS = [
    "Implement", "Design", "Test", "Review", "Deploy",
    "Refactor", "Document", "Integrate", "Migrate", "Configure",
    "Analyse", "Optimise", "Validate", "Monitor", "Audit",
]

TASK_NOUNS = [
    "DB schema", "REST API", "authentication module", "CI/CD pipeline",
    "frontend layout", "notification service", "cache layer", "search index",
    "reporting module", "admin panel", "data export", "user profile",
    "payment flow", "email service", "logging system",
]

ROLES = [
    "Developer", "Senior Developer", "Designer", "Business Analyst",
    "QA Engineer", "DevOps Engineer", "Solution Architect",
    "Project Manager", "Data Scientist", "Security Engineer",
]

MATERIAL_NAMES = [
    "Server", "Laptop", "Cloud License", "SSD Drive", "Network Switch",
    "UPS Unit", "Software License", "External HDD", "Monitor", "Keyboard",
]

TASK_STATUSES = ["pending", "in_progress", "completed", "on_hold"]
DEPENDENCY_TYPES = [
    "finish_to_start", "start_to_start", "finish_to_finish", "start_to_finish"
]

FIELDNAMES = [
    "record_type", "id", "name",
    "start_date", "end_date",
    "duration", "status", "project_id",
    "is_critical", "dependency_type",
    "resource_type", "role", "skill_level", "quantity",
    "task_id", "resource_id",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _empty_row() -> dict:
    return {f: "" for f in FIELDNAMES}


def _rand_date(start: date, end: date) -> date:
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, max(delta, 0)))


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

def generate(
    output_file: str,
    num_projects: int = 60,
    num_resources: int = 250,
    tasks_per_project: int = 14,
) -> int:
    rng = random.Random(42)  # deterministic seed for reproducibility
    rows: list[dict] = []

    # ---- Projects ----------------------------------------------------------
    project_ids: list[int] = []
    for i in range(1, num_projects + 1):
        start = _rand_date(date(2022, 1, 1), date(2024, 6, 1))
        end = start + timedelta(days=rng.randint(60, 730))
        prefix = rng.choice(PROJECT_PREFIXES)
        row = _empty_row()
        row.update(
            record_type="PROJECT",
            id=i,
            name=f"{prefix} {i}",
            start_date=str(start),
            end_date=str(end),
        )
        rows.append(row)
        project_ids.append(i)

    # ---- Resources ---------------------------------------------------------
    resource_ids: list[int] = []
    for i in range(1, num_resources + 1):
        row = _empty_row()
        if rng.random() < 0.65:
            row.update(
                record_type="HUMAN_RESOURCE",
                id=i,
                name=f"Person_{i}",
                resource_type="human",
                role=rng.choice(ROLES),
                skill_level=rng.randint(1, 10),
            )
        else:
            row.update(
                record_type="MATERIAL_RESOURCE",
                id=i,
                name=f"{rng.choice(MATERIAL_NAMES)}_{i}",
                resource_type="material",
                quantity=rng.randint(1, 500),
            )
        rows.append(row)
        resource_ids.append(i)

    # ---- Tasks + Milestones + Dependencies ---------------------------------
    task_id = 1
    task_ids: list[int] = []
    for project_id in project_ids:
        for _ in range(tasks_per_project):
            roll = rng.random()
            row = _empty_row()
            if roll < 0.12:
                row.update(
                    record_type="MILESTONE",
                    id=task_id,
                    name=f"Milestone_{task_id}",
                    duration=rng.randint(1, 5),
                    status=rng.choice(TASK_STATUSES),
                    project_id=project_id,
                    is_critical=rng.choice([True, False]),
                )
            elif roll < 0.22:
                row.update(
                    record_type="DEPENDENCY",
                    id=task_id,
                    name=f"Dependency_{task_id}",
                    duration=rng.randint(1, 10),
                    status=rng.choice(TASK_STATUSES),
                    project_id=project_id,
                    dependency_type=rng.choice(DEPENDENCY_TYPES),
                )
            else:
                verb = rng.choice(TASK_VERBS)
                noun = rng.choice(TASK_NOUNS)
                row.update(
                    record_type="TASK",
                    id=task_id,
                    name=f"{verb} {noun} #{task_id}",
                    duration=rng.randint(1, 30),
                    status=rng.choice(TASK_STATUSES),
                    project_id=project_id,
                )
            rows.append(row)
            task_ids.append(task_id)
            task_id += 1

    # ---- Assignments -------------------------------------------------------
    for t_id in task_ids:
        num_assigned = rng.randint(1, 3)
        assigned_resources = rng.sample(resource_ids, min(num_assigned, len(resource_ids)))
        for r_id in assigned_resources:
            row = _empty_row()
            row.update(
                record_type="ASSIGNMENT",
                task_id=t_id,
                resource_id=r_id,
            )
            rows.append(row)

    # ---- Pad to guarantee >= 1000 rows (edge cases) -----------------------
    while len(rows) < 1000:
        extra_proj_id = rng.choice(project_ids)
        row = _empty_row()
        row.update(
            record_type="TASK",
            id=task_id,
            name=f"Extra Task #{task_id}",
            duration=rng.randint(1, 20),
            status="pending",
            project_id=extra_proj_id,
        )
        rows.append(row)
        # Assign at least one resource
        r_id = rng.choice(resource_ids)
        assign_row = _empty_row()
        assign_row.update(record_type="ASSIGNMENT", task_id=task_id, resource_id=r_id)
        rows.append(assign_row)
        task_id += 1

    # ---- Write CSV ---------------------------------------------------------
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def main() -> None:
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    parser = argparse.ArgumentParser(
        description="Generate a multi-entity CSV file for the Project Planning System."
    )
    parser.add_argument(
        "--output",
        default=os.path.join(project_root, "data", "data.csv"),
        help="Output CSV file path (default: data/data.csv in project root)",
    )
    parser.add_argument("--projects", type=int, default=60, help="Number of projects (default: 60)")
    parser.add_argument("--resources", type=int, default=250, help="Number of resources (default: 250)")
    parser.add_argument(
        "--tasks-per-project", type=int, default=14, help="Tasks per project (default: 14)"
    )
    args = parser.parse_args()

    total = generate(
        output_file=args.output,
        num_projects=args.projects,
        num_resources=args.resources,
        tasks_per_project=args.tasks_per_project,
    )

    print(f"[generate_csv] Done. File: {args.output}")
    print(f"[generate_csv] Total rows written (excl. header): {total}")
    breakdown = {
        "PROJECT": args.projects,
        "RESOURCE": args.resources,
        "TASK/MILESTONE/DEPENDENCY": args.projects * args.tasks_per_project,
        "ASSIGNMENT": "~2x tasks",
    }
    for k, v in breakdown.items():
        print(f"  {k:<35} {v}")


if __name__ == "__main__":
    main()
