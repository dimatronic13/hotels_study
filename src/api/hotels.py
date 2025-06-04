from fastapi import Query, APIRouter, Body
from src.repositories  import HotelsRepository
from src.api.dependencies import PaginationDep
from src.database import async_session_maker
from src.schemas.hotels import HotelPATCH, HotelAdd

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

@hotel_router.get("/{hotel_id}")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@hotel_router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@hotel_router.post("")
async def create_hotel(hotel_data: HotelAdd = Body(openapi_examples={
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
        result = await HotelsRepository(session).add(hotel_data)
        await session.commit()

    return {"status": "OK", "data": result}



@hotel_router.put("/{hotel_id}")
async def replace_hotel(
        hotel_id: int,
        hotel_data: HotelAdd
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data=hotel_data,id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@hotel_router.patch("/{hotel_id}")
async def update_hotel(
        hotel_id: int,
        hotel_data: HotelPATCH
):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(data=hotel_data,id=hotel_id,exclude_unset=True)
        await session.commit()
    return {"status": "OK"}
