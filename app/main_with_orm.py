from fastapi import FastAPI
from .database import engine, Base, get_db
from .routers import post, user

app = FastAPI()

Base.metadata.create_all(bind=engine)

# testing


app.include_router(post.router)
app.include_router(user.router)

# @app.get("/testing")
# def get(db: Session = Depends(get_db)):
#     posts = db.query(Post).all()
#     return posts


# title->str and content->str
