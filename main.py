from fastapi import FastAPI, Query, Body
import uvicorn
from hotels import hotel_router
app = FastAPI(docs_url="/docs", redoc_url="")
app.include_router(hotel_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
