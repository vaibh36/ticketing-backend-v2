import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from tools import get_events, book_event

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

TOOLS = [
    {
        "type": "function",
        "name": "get_events",
        "description": "Get available events and seats.",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    },
    {
        "type": "function",
        "name": "book_event",
        "description": "Book seats for an event.",
        "parameters": {
            "type": "object",
            "properties": {
                "event_id": {
                    "type": "integer",
                    "description": "ID of the event"
                },
                "number_of_seats": {
                    "type": "integer",
                    "description": "Number of seats to book"
                },
                "user_name": {
                    "type": "string",
                    "description": "Id of the user"
                }
            },
            "required": [
                "event_id",
                "number_of_seats",
                "user_name"
            ]
        }
    }
]


def ask_agent(message: str) -> str:

    response = client.responses.create(
        model="gpt-5.5",
        instructions="""
        You are a ticket-booking assistant.

        Use get_events for event or seat availability.
        Use book_event when the user wants to book seats.

        Do not invent event or booking data.
        Answer briefly using tool results.
        """,
        input=message,
        tools=TOOLS
    )

    for item in response.output:

        if item.type != "function_call":
            continue

        if item.name == "get_events":

            events = get_events()

            small_events = [
                {
                    "id": event["id"],
                    "name": event["name"],
                    "available_seats": event["available_seats"]
                }
                for event in events
            ]

            tool_output = small_events

        elif item.name == "book_event":

            arguments = json.loads(item.arguments)

            event_id = arguments["event_id"]
            number_of_seats = arguments["number_of_seats"]
            user_name = arguments["user_name"]

            booking = book_event(
                event_id=event_id,
                number_of_seats=number_of_seats,
                user_name=user_name
            )

            tool_output = booking

        else:
            continue

        final_response = client.responses.create(
            model="gpt-5.5",
            previous_response_id=response.id,
            input=[
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": json.dumps(tool_output)
                }
            ]
        )

        return final_response.output_text

    return response.output_text