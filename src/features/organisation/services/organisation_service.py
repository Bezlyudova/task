from src.base.base_service import BaseService, BaseRepository
from src.features.organisation.repositories.organisation_repository import OrganisationRepository


class OrganisationService(BaseService):
    @property
    def repository(self) -> BaseRepository:
        return OrganisationRepository(self.req)
