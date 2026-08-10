from fastapi import FastAPI

from database import Base, engine
from models import Booking
from router import router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Booking Service"
)


app.include_router(router)


@app.get("/")
def home():
    return {
        "service": "booking-service",
        "message": "Booking Service is running"
    }