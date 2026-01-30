from fastapi import APIRouter
from pydantic import BaseModel
from ..db_models.users import signup_user, login_user

router = APIRouter()

## Signup Router
class SignupRequest(BaseModel):
    username: str
    password: str

@router.post("/signup")
def signup_api(payload: SignupRequest):
    success, message = signup_user(payload.username, payload.password)
    return {"success": success, "message": message}


##Login Router
class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
def login_api(payload: LoginRequest):
    success, message, user_id = login_user(
        payload.username, payload.password
    )
    return {"success": success, "message": message, "user_id": user_id}

