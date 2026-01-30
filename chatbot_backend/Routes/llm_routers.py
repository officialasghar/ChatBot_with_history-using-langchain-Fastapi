from fastapi import APIRouter
from pydantic import BaseModel
from ..LLM.chat_model import chat_endpoint 

router = APIRouter()

## Chat Router
class SignupRequest(BaseModel):
    user_id: int
    query: str

@router.post("/chat")
def chat_api(payload: SignupRequest):
    query_Response = chat_endpoint(payload.user_id, payload.query)
    return {"Response": query_Response}
