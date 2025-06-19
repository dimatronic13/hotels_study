from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class RoomsOrm(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]

    facility_links: Mapped[list["RoomsFacilitiesOrm"]] = relationship(
        back_populates="room",
        cascade="all, delete-orphan"
    )

    # Упрощённый доступ напрямую к удобствам (viewonly)
    facilities: Mapped[list["FacilitiesOrm"]] = relationship(
        secondary="rooms_facilities",
        back_populates="rooms",
        viewonly=True
    )