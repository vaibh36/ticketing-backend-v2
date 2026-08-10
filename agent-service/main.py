from fastapi import FastAPI

from router import router

app = FastAPI(
    title="Ticketing Agent Service"
)

app.include_router(router)


@app.get("/")
def health_check():
    return {
        "message": "Agent service is running"
    }