from typing import List, Optional
from sqlalchemy.orm import Session
from data_access.interfaces.i_resource_repository import IResourceRepository
from data_access.models.resource_model import ResourceModel


class ResourceRepository(IResourceRepository):

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_all(self) -> List[ResourceModel]:
        return self._session.query(ResourceModel).all()

    def get_by_id(self, resource_id: int) -> Optional[ResourceModel]:
        return self._session.query(ResourceModel).filter(ResourceModel.id == resource_id).first()

    def create(self, resource: ResourceModel) -> ResourceModel:
        self._session.add(resource)
        self._session.commit()
        self._session.refresh(resource)
        return resource

    def update(self, resource: ResourceModel) -> ResourceModel:
        merged = self._session.merge(resource)
        self._session.commit()
        self._session.refresh(merged)
        return merged

    def delete(self, resource_id: int) -> bool:
        resource = self.get_by_id(resource_id)
        if not resource:
            return False
        self._session.delete(resource)
        self._session.commit()
        return True

    def save_all(self, resources: List[ResourceModel]) -> List[ResourceModel]:
        self._session.add_all(resources)
        self._session.flush()
        self._session.commit()
        return resources
