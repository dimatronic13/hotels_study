from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.models.rooms import RoomsOrm
from src.schemas.facilities import RoomFacilityAdd
from src.schemas.rooms import RoomAdd, RoomAddRequest, RoomPatchRequest, RoomPatch

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int,
                    db: DBDep,
                    date_from: date = Query(example="2025-07-01"),
                    date_to: date = Query(example="2025-08-01"),
                    ):

    result =  await db.rooms.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        hotel_id=hotel_id,
        load_facilities=True,
    )
    return result


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    result = await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id,load_facilities=True)
    return result


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id:int, db: DBDep, room_data: RoomAddRequest = Body()
):

    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    print(_room_data)
    room = await db.rooms.add(_room_data)

    rooms_facilities_data = [RoomFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(rooms_facilities_data)
    await db.commit()

    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/room/{room_id}")
async def replace_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest,
        db: DBDep,
):
    await db.rooms.update_room_with_facilities(
        room_id=room_id,
        hotel_id=hotel_id,
        room_data=room_data,
        facilities_repo=db.facilities
    )
    await db.commit()

    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id, load_facilities=True)


@router.patch("/{hotel_id}/room/{room_id}")
async def update_room(
    hotel_id: int,
    room_id: int,
    room_data: RoomPatchRequest,
    db: DBDep
):
    await db.rooms.patch_room_with_facilities(
        room_id=room_id,
        hotel_id=hotel_id,
        room_data=room_data,
        facilities_repo=db.facilities
    )
    await db.commit()
    return await db.rooms.get_one_or_none(id=room_id, hotel_id=hotel_id, load_facilities=True)
