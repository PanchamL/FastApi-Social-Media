import random
from typing import Optional
from fastapi import FastAPI,HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND


app = FastAPI()



class Post(BaseModel):
    title : str
    content : str
    published : bool = True


while True:
    try:
        conn = psycopg2.connect(host= 'localhost', database='fastapi', user='postgres', password='madmamu', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database Connection Succesfull")
        break
    except Exception as error:
        print("Connection Failed")
        print("error was: ", error)
        time.sleep(2)



def find_post(id):
    for p in posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(posts):
        if p["id"] == id:
            return i


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM POSTS """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}
    

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()

    conn.commit() # commit to change

    return {"data" :new_post}

@app.get("/posts/latest")
def latest_post():
    post = my_posts[len(my_posts)-1]
    return {"update": f"{post}"}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM POSTS WHERE id =%s;""", (str(id)))
    test_post = cursor.fetchone()

    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"The post with id : {id} doesn't exist")
    return {"post" : test_post}

@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def del_post(id: int):
    post_del = find_post(id)
    if not post_del:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"The post with id : {id} doesn't exist")
    else:
        my_posts.remove(post_del)
        return {"update": f"Post with {id} is deleted"}

@app.put("/posts/{id}")
def update_post(id:int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"The post with id : {id} doesn't exist")
    else:
        post_dict = post.dict()
        post_dict['id'] = id
        my_posts[index] = post_dict
        return {"post" : post_dict}
