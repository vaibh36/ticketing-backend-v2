import os
import httpx

EVENT_SERVICE_URL = os.getenv(
    "EVENT_SERVICE_URL",
    "http://localhost:8001"
)

BOOKING_SERVICE_URL = os.getenv(
    "BOOKING_SERVICE_URL",
    "http://localhost:8002"
)


def get_events():
    url = f"{EVENT_SERVICE_URL}/events/"

    response = httpx.get(url)

    if response.status_code != 200:
        return {
            "error": "Unable to fetch events"
        }

    return response.json()


def book_event(event_id: int, number_of_seats: int, user_name: str):
    url = f"{BOOKING_SERVICE_URL}/bookings/"

    payload = {
        "event_id": event_id,
        "number_of_seats": number_of_seats,
        "user_name": user_name
    }

    response = httpx.post(
        url,
        json=payload
    )

    if response.status_code not in [200, 201]:
        return {
            "error": "Unable to create booking"
        }

    return response.json()