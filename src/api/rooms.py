from fastapi import APIRouter, Body

from fastapi import APIRouter, Body

from src.api.dependencies import DBDep
from src.schemas.rooms import RoomAdd, RoomPATCH, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, db: DBDep):
    return await db.rooms.get_filtered(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int, db: DBDep):
    return await db.rooms.get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_hotel(hotel_id: int, room_id: int, db: DBDep):
    await db.rooms.delete(id=room_id, hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.post("/{hotel_id}/rooms")
async def create_room(hotel_id:int, db: DBDep, room_data: RoomAddRequest = Body(openapi_examples={
    "1": {
        "summary": "Room Sea",
        "value": {
            "hotel_id": "1",
            "title": "Room Sea side",
            "description": "With Sea view",
            "price": 10000,
            "quantity": 10
        }
    },
    "2": {
        "summary": "Room Mountains",
        "value": {
            "hotel_id": "3",
            "title": "Room Mountain side",
            "description": "With Mountain view.",
            "price": 17000,
            "quantity": 10
        }
    }
})
):
    _room_data = RoomAdd(hotel_id= hotel_id ,**room_data.model_dump())
    result = await db.rooms.add(_room_data)
    await db.commit()
    return {"status": "OK", "data": result}


@router.put("/{hotel_id}/room/{room_id}")
async def replace_hotel(
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest,
        db: DBDep,
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(data=_room_data, id=room_id,hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/room/{room_id}")
async def update_hotel(
        hotel_id:int,
        room_id: int,
        room_data: RoomPatchRequest,
        db: DBDep,
):
    _room_data = RoomPATCH(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(data=_room_data, id=room_id, exclude_unset=True,hotel_id=hotel_id)
    await db.commit()
    return {"status": "OK"}
