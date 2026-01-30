from .Routes.user_routers import router as signup_login_routers
from .Routes.llm_routers import router as chat_routers
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI
app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins for local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(signup_login_routers)
app.include_router(chat_routers)