from fastapi import Query, Body, APIRouter
from schemas.hotels import Hotel, HotelPATCH
import math

hotel_router = APIRouter(prefix="/hotels", tags=["Hotels"])
hotels = [
    {"id": 1, "title": "Sochi", "name": "Sochi-RSL"},
    {"id": 2, "title": "Дубай", "name": "Dubai"},
    {"id": 3, "title": "Мальдивы", "name": "maldivi"},
    {"id": 4, "title": "Геленджик", "name": "gelendzhik"},
    {"id": 5, "title": "Москва", "name": "moscow"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Санкт-Петербург", "name": "spb"},
]

PAGE = 1
PER_PAGE = 3


@hotel_router.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
        page: int = PAGE,
        per_page: int = PER_PAGE
):
    hotels_ = []
    if page < PAGE:
        page = PAGE
    if per_page < 1:
        per_page = PER_PAGE
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    pages_count = math.ceil(len(hotels_) / per_page)
    page = min(pages_count, page)
    hotels_slice = hotels_[(page - 1) * per_page:page * per_page]
    pages_count_dict = {"page": page, "pages": pages_count}
    hotels_slice.append(pages_count_dict)
    return hotels_slice


@hotel_router.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@hotel_router.post("/hotels")
def create_hotel(hotel_data: Hotel):
    global hotels
    hotels.routerend({
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
