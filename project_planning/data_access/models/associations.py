"""
Association table for the many-to-many relationship between Task and Resource.
Defined here to avoid circular imports between task_model and resource_model.
"""
from sqlalchemy import Table, Column, Integer, ForeignKey
from infrastructure.database import Base

task_resource_association = Table(
    "task_resources",
    Base.metadata,
    Column("task_id", Integer, ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
    Column("resource_id", Integer, ForeignKey("resources.id", ondelete="CASCADE"), primary_key=True),
)
