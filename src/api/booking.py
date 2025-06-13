from fastapi import APIRouter, Body, HTTPException

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.booking import BookingAddRequest, Booking, BookingAdd

router = APIRouter(prefix="/booking", tags=["Бронирование"])


@router.get("/")
async def get_bookings( db: DBDep, user_id: UserIdDep,):
    return await db.bookings.get_filtered(user_id=user_id)



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
    if not user_id or not room_id:
        HTTPException(detail="User id or room id is required", status_code=401)
    rooms = await db.rooms.get_filtered(id=room_id)
    price = rooms[0].price
    print(price, user_id, room_id)
    _booking_data = BookingAdd(user_id = user_id , price=price, **booking_data.model_dump())
    result = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": result}



