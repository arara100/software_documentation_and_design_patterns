from typing import List, Optional
from sqlalchemy.orm import Session
from data_access.interfaces.i_project_repository import IProjectRepository
from data_access.models.project_model import ProjectModel


class ProjectRepository(IProjectRepository):

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_all(self) -> List[ProjectModel]:
        return self._session.query(ProjectModel).all()

    def get_by_id(self, project_id: int) -> Optional[ProjectModel]:
        return self._session.query(ProjectModel).filter(ProjectModel.id == project_id).first()

    def create(self, project: ProjectModel) -> ProjectModel:
        self._session.add(project)
        self._session.commit()
        self._session.refresh(project)
        return project

    def update(self, project: ProjectModel) -> ProjectModel:
        merged = self._session.merge(project)
        self._session.commit()
        self._session.refresh(merged)
        return merged

    def delete(self, project_id: int) -> bool:
        project = self.get_by_id(project_id)
        if not project:
            return False
        self._session.delete(project)
        self._session.commit()
        return True

    def save_all(self, projects: List[ProjectModel]) -> List[ProjectModel]:
        self._session.add_all(projects)
        self._session.flush()
        self._session.commit()
        return projects
