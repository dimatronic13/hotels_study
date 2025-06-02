from fastapi import FastAPI
import uvicorn
from src.api.hotels import hotel_router
from src.config import settings

from src.api.auth import router as auth_router
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

app = FastAPI(docs_url="/docs", redoc_url="")
app.include_router(auth_router)
app.include_router(hotel_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
