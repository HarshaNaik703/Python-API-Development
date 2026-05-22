from fastapi import FastAPI
from .database import engine, Base, get_db
from .routers import post, user, auth

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
