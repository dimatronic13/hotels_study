import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

from src.api.auth import router as auth_router
from src.api.hotels import router as hotels_router
from src.api.rooms import router as room_router
from src.api.bookings import router as bookings_router
from src.api.facilities import router as facilities_router
sys.path.append(str(Path(__file__).parent.parent))

app = FastAPI(docs_url="/docs", redoc_url="")
app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(room_router)
app.include_router(bookings_router)
app.include_router(facilities_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
