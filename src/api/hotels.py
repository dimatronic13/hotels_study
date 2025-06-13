from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPATCH, HotelAdd

hotel_router = APIRouter(prefix="/hotels", tags=["Отели"])


@hotel_router.get("")
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Location"),
):
    per_page = pagination.per_page or 5
    return await db.hotels.get_all(
        location=location,
        title=title,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@hotel_router.get("/{hotel_id}")
async def get_hotel(hotel_id: int, db: DBDep):
     return await db.hotels.get_one_or_none(id=hotel_id)


@hotel_router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@hotel_router.post("")
async def create_hotel(db: DBDep, hotel_data: HotelAdd = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель Rich 5 звезд",
            "location": "Сочи , ул. Моря, 1",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель У фонтана",
            "location": "Дубай, ул. Шейха, 2",
        }
    }
})
):
    result = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": result}


@hotel_router.put("/{hotel_id}")
async def replace_hotel(
        hotel_id: int,
        hotel_data: HotelAdd,
        db: DBDep
):
    await db.hotels.edit(data=hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@hotel_router.patch("/{hotel_id}")
async def update_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH,
        db: DBDep
):
    await db.hotels.edit(data=hotel_data, id=hotel_id, exclude_unset=True)
    await db.commit()
    return {"status": "OK"}
