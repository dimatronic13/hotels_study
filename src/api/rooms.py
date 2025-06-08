from typing import List

from fastapi import Query, APIRouter, Body

from src.database import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import Room, RoomAdd, RoomPATCH

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms", response_model=List[Room])
async def get_rooms(hotel_id=None):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(
            hotel_id=hotel_id
        )


@router.get("/{hotel_id}/room/{room_id}", response_model=Room)
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.delete("/{hotel_id}/room/{room_id}", response_model=Room)
async def delete_hotel(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(id=room_id,hotel_id=hotel_id)
        await session.commit()
    return {"status": "OK"}

@router.post("/{hotel_id}/rooms")
async def create_room(room_data: RoomAdd = Body(openapi_examples={
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
    async with async_session_maker() as session:
        result = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": result}

@router.put("/{hotel_id}/room/{room_id}")
async def replace_hotel(
        room_id: int,
        room_data: RoomAdd
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=room_data,id=room_id)
        await session.commit()
    return {"status": "OK"}

@router.patch("/{hotel_id}/room/{room_id}")
async def update_hotel(
        room_id: int,
        room_data: RoomPATCH
):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(data=room_data,id=room_id,exclude_unset=True)
        await session.commit()
    return {"status": "OK"}
