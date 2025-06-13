from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("/bookings/me")
async def get_bookings( db: DBDep, user_id: UserIdDep,):
    return await db.bookings.get_filtered(user_id=user_id)


@router.get("/bookings")
async def get_bookings( db: DBDep, user_id: UserIdDep,):
    return await db.bookings.get_all()



@router.post("/")
async def create_booking(room_id:int,
                         db: DBDep,
                         user_id: UserIdDep,
                         booking_data: BookingAddRequest = Body(openapi_examples={
    "1": {
        "summary": "Two weeks at sea",
        "value": {
            "room_id": "1",
            "date_from": "2025-07-01",
            "date_to": "2025-07-15"
        }
    },
    "2": {
        "summary": "One week",
        "value": {
            "room_id": "3",
            "date_from": "2025-07-01",
            "date_to": "2025-07-08"
        }
    }
})
):
    room = await db.rooms.get_one_or_none(id=room_id)
    price = room.price
    _booking_data = BookingAdd(user_id = user_id,
                               price=price,
                               **booking_data.model_dump())
    result = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": result}



