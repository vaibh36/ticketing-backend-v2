from fastapi import APIRouter

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