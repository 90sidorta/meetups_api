from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import attends, meetups, users, auth

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(meetups.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(attends.router)
