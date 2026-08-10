from fastapi import FastAPI

from database import Base, engine
from models import Event
from router import router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Event Service"
)


app.include_router(router)


@app.get("/")
def home():
    return {
        "service": "event-service",
        "message": "Event Service is running"
    }