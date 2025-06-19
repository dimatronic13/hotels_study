from datetime import date

from sqlalchemy import select, update, delete, insert
from sqlalchemy.orm import selectinload

from src.models.facilities import RoomsFacilitiesOrm
from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.repositories.facilities import FacilitiesRepository
from src.repositories.utils import rooms_ids_for_booking
from src.schemas.rooms import Room, RoomPatchRequest, RoomPatch


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    async def get_filtered_by_time(
            self,
            hotel_id,
            date_from: date,
            date_to: date,
            load_facilities=False,
    ):
        rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
        return await self.get_filtered(load_facilities,RoomsOrm.id.in_(rooms_ids_to_get),)

    async def get_filtered(self,load_facilities=False, *filter, **filter_by):
        query = (
            select(self.model)
            .filter(*filter)
            .filter_by(**filter_by)
        )
        if load_facilities:
            query = query.options(selectinload(self.model.facilities))
        result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_one_or_none(self,load_facilities=False,  **filter_by):
        query = select(self.model).filter_by(**filter_by)
        if load_facilities:
            query = query.options(selectinload(self.model.facilities))
        result = await self.session.execute(query)
        model = result.scalars().one_or_none()
        if model is None:
            return None
        return self.schema.model_validate(model)

    async def sync_room_facilities(
            self,
            room_id: int,
            facilities_ids: list[int],
            facilities_repo: FacilitiesRepository
    ):
        incoming_ids = set(facilities_ids)
        existing_ids = await facilities_repo.get_existing_ids(list(incoming_ids))

        missing_ids = incoming_ids - existing_ids
        if missing_ids:
            raise ValueError(f"Некорректные facility_id: {sorted(missing_ids)}")

        query = select(RoomsFacilitiesOrm.facility_id).where(RoomsFacilitiesOrm.room_id == room_id)
        result = await self.session.execute(query)
        current_ids = set(result.scalars().all())

        to_add = existing_ids - current_ids
        to_delete = current_ids - existing_ids

        if to_delete:
            await self.session.execute(
                delete(RoomsFacilitiesOrm).where(
                    RoomsFacilitiesOrm.room_id == room_id,
                    RoomsFacilitiesOrm.facility_id.in_(to_delete)
                )
            )

        if to_add:
            insert_data = [
                {"room_id": room_id, "facility_id": fid}
                for fid in to_add
            ]
            await self.session.execute(insert(RoomsFacilitiesOrm).values(insert_data))

    async def update_room_with_facilities(
        self,
        room_id: int,
        hotel_id: int,
        room_data: RoomPatchRequest,
        facilities_repo: FacilitiesRepository
    ):
        # 1. Обновить комнату
        update_data = room_data.model_dump(exclude_unset=True, exclude={"facilities_ids"})

        if update_data:
            await self.session.execute(
                update(RoomsOrm)
                .where(RoomsOrm.id == room_id, RoomsOrm.hotel_id == hotel_id)
                .values(**update_data)
            )

        # 2. Обновить связи facilities
        if room_data.facilities_ids is not None:
            await self.sync_room_facilities(
                room_id=room_id,
                facilities_ids=room_data.facilities_ids,
                facilities_repo=facilities_repo
            )
    async def patch_room_with_facilities(
        self,
        room_id: int,
        hotel_id: int,
        room_data: RoomPatchRequest,
        facilities_repo: FacilitiesRepository
    ):

        update_data = room_data.model_dump(exclude_unset=True, exclude={"facilities_ids"})
        if update_data:
            patch = RoomPatch(hotel_id=hotel_id, **update_data)
            await self.edit(data=patch, id=room_id, hotel_id=hotel_id, exclude_unset=True)

        if room_data.facilities_ids is not None:
            await self.sync_room_facilities(
                room_id=room_id,
                facilities_ids=room_data.facilities_ids,
                facilities_repo=facilities_repo
            )
