from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infrastructure.database import Base
from data_access.models.associations import task_resource_association


class ResourceModel(Base):
    """
    Abstract Resource mapped to a single table (single-table inheritance via resource_type).
      - "human"    — HumanResource (role, skill_level)
      - "material" — MaterialResource (quantity)
    """
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    resource_type = Column(String(20), nullable=False)  # human / material

    # HumanResource fields
    role = Column(String(100), nullable=True)
    skill_level = Column(Integer, nullable=True)

    # MaterialResource fields
    quantity = Column(Integer, nullable=True)

    tasks = relationship(
        "TaskModel",
        secondary=task_resource_association,
        back_populates="resources",
        lazy="select",
    )

    def __repr__(self) -> str:
        return f"<Resource id={self.id} name={self.name!r} type={self.resource_type}>"
