from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey

from src.database import Base


class FacilitiesOrm(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    room_links: Mapped[list["RoomsFacilitiesOrm"]] = relationship(
        back_populates="facility",
        cascade="all, delete-orphan"
    )

    rooms: Mapped[list["RoomsOrm"]] = relationship(
        secondary="rooms_facilities",
        back_populates="facilities",
        viewonly=True
    )

class RoomsFacilitiesOrm(Base):
    __tablename__ = "rooms_facilities"
    room_id: Mapped[int] = mapped_column(ForeignKey("rooms.id", ondelete="CASCADE"), primary_key=True)
    facility_id: Mapped[int] = mapped_column(ForeignKey("facilities.id", ondelete="CASCADE"), primary_key=True)
    room: Mapped["RoomsOrm"] = relationship(back_populates="facility_links")
    facility: Mapped["FacilitiesOrm"] = relationship(back_populates="room_links")