from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAddRequest, BookingAdd
from src.schemas.facilities import FacilityAddRequest

router = APIRouter(prefix="/facilities", tags=["Удобства"])



@router.get("/")
async def get_facilities( db: DBDep):
    return await db.facilities.get_all()



@router.post("/")
async def create_facility(db: DBDep,
                         facility_data: FacilityAddRequest = Body(openapi_examples={
    "1": {
        "summary": "Shower",
        "value": {
            "title": "Shower",
        }
    },
    "2": {
        "summary": "Parking",
        "value": {
            "title": "Parking",
        }
    },
                             "3": {
                                 "summary": "Free WiFi",
                                 "value": {
                                     "title": "Free WiFi",
                                 }
                             }
})
):
    result = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": result}



