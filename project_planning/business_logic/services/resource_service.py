from typing import List, Optional

from business_logic.interfaces.i_resource_service import IResourceService
from data_access.interfaces.i_resource_repository import IResourceRepository
from data_access.models.resource_model import ResourceModel


class ResourceService(IResourceService):
    """
    Business logic for Resources.
    Depends on DAL interface only — concrete repository is injected via DI.
    """

    def __init__(self, resource_repo: IResourceRepository) -> None:
        self._resource_repo = resource_repo

    # ------------------------------------------------------------------ #

    def get_all_resources(self) -> List[ResourceModel]:
        return self._resource_repo.get_all()

    def get_resource(self, resource_id: int) -> Optional[ResourceModel]:
        return self._resource_repo.get_by_id(resource_id)

    def create_human_resource(
        self, name: str, role: str, skill_level: int
    ) -> ResourceModel:
        resource = ResourceModel(
            name=name,
            resource_type="human",
            role=role,
            skill_level=skill_level,
        )
        return self._resource_repo.create(resource)

    def create_material_resource(
        self, name: str, quantity: int
    ) -> ResourceModel:
        resource = ResourceModel(
            name=name,
            resource_type="material",
            quantity=quantity,
        )
        return self._resource_repo.create(resource)

    def update_resource(self, resource_id: int, **kwargs) -> Optional[ResourceModel]:
        resource = self._resource_repo.get_by_id(resource_id)
        if not resource:
            return None
        allowed = {"name", "role", "skill_level", "quantity"}
        for key, value in kwargs.items():
            if key in allowed:
                setattr(resource, key, value)
        return self._resource_repo.update(resource)

    def delete_resource(self, resource_id: int) -> bool:
        return self._resource_repo.delete(resource_id)
