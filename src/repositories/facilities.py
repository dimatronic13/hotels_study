from datetime import date

from sqlalchemy import select

from src.repositories.base import BaseRepository
from src.models.facilities import FacilitiesOrm , RoomsFacilitiesOrm
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesOrm
    schema = Facility

    async def get_existing_ids(self, ids: list[int]) -> set[int]:
        if not ids:
            return set()
        query = select(self.model.id).where(self.model.id.in_(ids))
        result = await self.session.execute(query)
        return set(result.scalars().all())

class RoomFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesOrm
    schema = RoomFacility
