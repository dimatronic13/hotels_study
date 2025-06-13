from src.repositories.base import BaseRepository
from src.models.booking import BookingsOrm
from src.schemas.booking import Booking


class BookingRepository(BaseRepository):
    model = BookingsOrm
    schema = Booking
