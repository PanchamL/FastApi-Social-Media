import random
from typing import Optional
from fastapi import FastAPI,HTTPException, status
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange


from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND


app = FastAPI()



class Post(BaseModel):
    id = randrange(0,10000)
    title : str
    content : str
    rating : Optional[int] = None

my_posts = [{"title": "title 1", "content" : "content1", "id": 1},{"title": "title 2", "content" : "content2", "id": 2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}
    

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(1,10000)
    my_posts.append(post_dict)
    return {"data" :post_dict}

@app.get("/posts/latest")
def latest_post():
    post = my_posts[len(my_posts)-1]
    return {"update": f"{post}"}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"The post with id : {id} doesn't exist")
    return {"post" : post}

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
