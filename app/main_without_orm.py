from fastapi import FastAPI, HTTPException, status
from fastapi.params import Body
from typing import Optional
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
import time
app = FastAPI()

# title->str and content->str
class Post(BaseModel):
    title:str
    content:str
    

class UpdatePost(Post):
    rating : int
    

while True:
    try:
        conn = psycopg2.connect(
            dbname="fastapi",
            user="harsha",
            password="mypassword",
            host="localhost",
            cursor_factory=RealDictCursor
        )
        cur = conn.cursor()
        print("database connection is successful")
        break
    except Exception as err:
        print("failed to connect")
        print(f"Error is : {err}") 
        time.sleep(2)




# print(records)
post_array = []

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    cur.execute("SELECT id,title, content, published, rating FROM posts")
    posts = cur.fetchall()
    return posts


@app.post("/create_post", status_code=status.HTTP_201_CREATED)
def create_post(post:Post ): 
    if post is None:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT)
    cur.execute("""insert into posts (title,content) values (%s ,%s) RETURNING *""",(post.title, post.content))
    newpost = cur.fetchone()
    conn.commit()
    return {"message":f"successfully cre ated the post named \"{post.title}\""}


@app.get("/post/{id}")
def get_post(id: int, status_code = status.HTTP_200_OK):
    cur.execute(
        "SELECT id,title, content, published, rating FROM posts",
        (id,)
    )
    post = cur.fetchone()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return post

@app.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cur.execute(
        "delete from posts where id = %s returning *",
        (id,)
    )
    post = cur.fetchone()
    if post is None:
        raise HTTPException(status_code =status.HTTP_404_NOT_FOUND, detail="Not found")
    conn.commit()
    return

@app.put("/update/{id}", status_code=status.HTTP_205_RESET_CONTENT)
def update(id:int, post:UpdatePost):
    if id is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    cur.execute(
        "SELECT * FROM posts WHERE id = %s",
        (id,)
    )
    temp = cur.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    cur.execute("""update posts 
                    set title = %s, content = %s, rating = %s
                    where id = %s
                    returning *
                    """,
                (post.title, post.content, post.rating,id))
    cur.fetchone()
    conn.commit()
    return {"messaeg":"successfully updated"}
        
