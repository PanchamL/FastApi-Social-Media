from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import pydantic
from pydantic import BaseModel, __dict__, DictError
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session, session
from . import models
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()



class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:

    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
                                password='madmamu', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)


@app.get("/")
def root():
    return {"message": "Hello World"}





@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
    return {"status": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, db: Session= Depends(get_db)):
    
    posts = db.query(models.Post).filter(models.Post.id == id).one()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    return {"post_detail": posts}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    else:
        deleted_post.delete(synchronize_session=False)
        db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int,updated_post: Post, db : Session= Depends(get_db),):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    new_post = post_query.first()
    print()
    if new_post  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")

    post_query.update(updated_post.dict() , synchronize_session=False)

    db.commit()

    return {"data": updated_post}