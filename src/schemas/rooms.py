from pydantic import BaseModel, ConfigDict, Field


class RoomAdd(BaseModel):
    hotel_id: int
    title: str
    description: str | None
    price: int
    quantity: int


class RoomPATCH(BaseModel):
    title: str | None = Field(None)
    description: str | None = Field(None)
    price: int | None = Field(None)
    quantity: int | None = Field(None)


class Room(RoomAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)