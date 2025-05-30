from fastapi import Query, APIRouter, Body

from src.api.dependencies import PaginationDep
from src.schemas.hotels import Hotel, HotelPATCH

hotel_router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Sochi", "name": "sochi"},
    {"id": 2, "title": "Дубай", "name": "dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]


@hotel_router.get("/hotels")
def get_hotels(
        pagination: PaginationDep,
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    if pagination.page and pagination.per_page:
        return hotels_[pagination.per_page * (pagination.page-1):][:pagination.per_page]
    return hotels_


@hotel_router.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@hotel_router.post("/hotels")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {
        "summary": "Сочи",
        "value": {
            "title": "Отель Сочи 5 звезд у моря",
            "name": "sochi_u_morya",
        }
    },
    "2": {
        "summary": "Дубай",
        "value": {
            "title": "Отель Дубай У фонтана",
            "name": "dubai_fountain",
        }
    }
})
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
    return {"status": "OK"}


@hotel_router.put("/hotels/{hotel_id}")
def replace_hotel(
        hotel_id: int,
        hotel_data: Hotel
):
    global hotels
    hotels = [{"id": hotel_id, "name": hotel_data.name, "title": hotel_data.title} if _["id"] == hotel_id else _ for _
              in hotels]
    return {"status": "OK"}


@hotel_router.patch("/hotels/{hotel_id}")
def update_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    global hotels
    for index, hotel in enumerate(hotels):
        if hotel["id"] != hotel_id:
            continue
        if hotel_data.title and hotel["title"] != hotel_data.title and hotel_data.title != "string":
            hotels[index]["title"] = hotel_data.title
        if hotel_data.name and hotel["name"] != hotel_data.name and hotel_data.name != "string":
            hotels[index]["name"] = hotel_data.name

    return {"status": "OK"}
