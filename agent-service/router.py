from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from schemas import AgentRequest, AgentResponse
from service import ask_agent


router = APIRouter(
    prefix="/agent",
    tags=["Agent"]
)


@router.post("/chat", response_model=AgentResponse)
def chat(request: AgentRequest):

    response = ask_agent(request.message)

    return AgentResponse(
        response=response
    )


@router.websocket("/ws")
async def agent_websocket(websocket: WebSocket):

    await websocket.accept()

    try:
        while True:
            message = await websocket.receive_text()

            response = ask_agent(message)

            await websocket.send_json(
                {
                    "type": "message",
                    "content": response
                }
            )

    except WebSocketDisconnect:
        print("WebSocket disconnected")