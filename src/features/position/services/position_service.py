from src.base.base_service import BaseService, BaseRepository
from src.features.position.repositories.position_repository import PositionRepository


class PositionService(BaseService):
    @property
    def repository(self) -> BaseRepository:
        return PositionRepository(self.req)
