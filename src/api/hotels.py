from fastapi import Query, APIRouter, Body
from sqlalchemy import insert, select, func

from src.api.dependencies import PaginationDep
from src.database import async_session_maker, engine
from src.models.hotels import HotelsOrm
from src.schemas.hotels import Hotel, HotelPATCH
from repositories.hotels import HotelsRepository

hotel_router = APIRouter(prefix="/hotels", tags=["Отели"])

@hotel_router.get("")
async def get_hotels(
        pagination: PaginationDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Location"),
):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            location=location,
            title=title,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )



@hotel_router.delete("/{hotel_id}")
def delete_hotel(hotel_id: int):
#    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@hotel_router.post("")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
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
    async with async_session_maker() as session:
        # add_hotel_stmt = insert(HotelsOrm).values(**hotel_data.model_dump())
        # await session.execute(add_hotel_stmt)
        result = await HotelsRepository(session).create(hotel_data)
        await session.commit()

    return {"status": "OK", "data": result}



@hotel_router.put("/{hotel_id}")
def replace_hotel(
        hotel_id: int,
        hotel_data: Hotel
):
    # hotels = [{"id": hotel_id, "name": hotel_data.name, "title": hotel_data.title} if _["id"] == hotel_id else _ for _
    #           in hotels]
    return {"status": "OK"}


@hotel_router.patch("/{hotel_id}")
def update_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    for index, hotel in enumerate(hotels):
        if hotel["id"] != hotel_id:
            continue
        if hotel_data.title and hotel["title"] != hotel_data.title and hotel_data.title != "string":
            hotels[index]["title"] = hotel_data.title
        if hotel_data.name and hotel["name"] != hotel_data.name and hotel_data.name != "string":
            hotels[index]["name"] = hotel_data.name

    return {"status": "OK"}
