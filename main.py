from fastapi import FastAPI, Query, Body
import uvicorn

app = FastAPI(docs_url="/docs", redoc_url="")

hotels = [
    {"id": 1, "title": "Sochi", "name": "Sochi-RSL"},
    {"id": 2, "title": "Дубай", "name": "Dubai"},
    {"id": 3, "title": "New York", "name": "New York"}
]


@app.get("/hotels")
def get_hotels(
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
    return hotels_


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True),
    ):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}


@app.put("/hotels/{hotel_id}")
def replace_hotel(
        hotel_id: int,
        title: str = Body(embed=True),
        name: str = Body(embed=True),
):
    global hotels
    hotels = [{"id": hotel_id, "name": name, "title": title} if _["id"] == hotel_id else _ for _ in hotels]
    return {"status": "OK"}


@app.patch("/hotels/{hotel_id}")
def update_hotel(
        hotel_id: int,
        title: str | None = Body(default=None, embed=True),
        name: str | None = Body(default=None, embed=True),
    ):
    global hotels
    for index, hotel in enumerate(hotels):
        if hotel["id"] != hotel_id:
            continue
        if title and hotel["title"] != title and title != "string":
            hotels[index]["title"] = title
        if name and hotel["name"] != name and name != "string":
            hotels[index]["name"] = name

    return {"status": "OK"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
