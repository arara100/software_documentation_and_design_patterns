from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.database import Base
from data_access.models.associations import task_resource_association


class TaskModel(Base):
    """
    Represents a generic Task.
    Milestones and Dependencies are stored in the same table via `task_type` discriminator:
      - "task"        — regular task
      - "milestone"   — milestone (uses is_critical)
      - "dependency"  — dependency (uses dependency_type)
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    duration = Column(Integer, nullable=False, default=1)
    status = Column(String(50), nullable=False, default="pending")
    task_type = Column(String(20), nullable=False, default="task")

    # Milestone-specific
    is_critical = Column(Boolean, nullable=True)

    # Dependency-specific
    dependency_type = Column(String(50), nullable=True)

    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    project = relationship("ProjectModel", back_populates="tasks")

    resources = relationship(
        "ResourceModel",
        secondary=task_resource_association,
        back_populates="tasks",
        lazy="select",
    )

    def __repr__(self) -> str:
        return f"<Task id={self.id} name={self.name!r} type={self.task_type}>"
