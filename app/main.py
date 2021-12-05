from psycopg2.extras import RealDictCursor
import time
import psycopg2
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
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





@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}
    

@app.post("/posts", status_code= status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()

    conn.commit() # commit to change

    return {"data" :new_post}


@app.get("/posts/latest", status_code = status.HTTP_200_OK)
def latest_post():
    cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")
    recent_post = cursor.fetchone()
    return {"update": recent_post}


@app.get("/posts/{id}", status_code= status.HTTP_201_CREATED)
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id =%s;""", (str(id)))
    test_post = cursor.fetchone()

    if not test_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = f"The post with id : {id} doesn't exist")
    return {"post" : test_post}



@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def del_post(id: int):

    cursor.execute("""DELETE FROM posts where id = %s RETURNING *""", (str(id)))
    delete_post = cursor.fetchone()
    if delete_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"The post with id : {id} doesn't exist")
    else:
        return {"update": delete_post}



@app.put("/posts/{id}", status_code=status.HTTP_205_RESET_CONTENT)
def update_post(id:int, post: Post):

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id= %s RETURNING *""", (post.title, post.content, str(id), post.published))
    updated_post = cursor.fetchone()

    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail = f"The post with id : {id} doesn't exist")
    else:
         return {"post" : updated_post}
