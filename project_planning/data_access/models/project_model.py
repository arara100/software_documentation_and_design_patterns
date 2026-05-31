from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from infrastructure.database import Base


class ProjectModel(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    tasks = relationship(
        "TaskModel",
        back_populates="project",
        cascade="all, delete-orphan",
        lazy="select",
    )

    def __repr__(self) -> str:
        return f"<Project id={self.id} name={self.name!r}>"
