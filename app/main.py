from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body

from pydantic import BaseModel
from typing import Optional

from random import randrange


import psycopg2
# from psycopg2 import Error, RealDictCursor

import time




app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password="root",
            port=5432,
        )
        cursor = conn.cursor()
        print("Connected to the database")
        break
    except Exception as e:
        print("Error connecting to the database:", e)
    time.sleep(2)




class Post(BaseModel):
    title: str
    content: str
    age: int
    time: str = None
    






dummy_posts = [
         {"id":1,"title": "title1", "content": "content1", "age": 1, "time": "time1"},
         {"id":2,"title": "title2", "content": "content2", "age": 2, "time": "time2"},
         {"id":3,"title": "title3", "content": "content3", "age": 3, "time": "time3"}]


@app.get("/")
async def root():
    return {"message": "Hello Worldss"}


@app.get('/post/')
async def payload():
    try:
        print(payload,'---------')
        # return {"DATA":'teststst',"status":200,'message':'success','data':payload.get('time')}

        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()

        print(posts,'---------')

        return {"posts":posts}
    except Exception as e:
        print("error------->>>> ",e)
        return {"posts":e}




# USING DATABASE POST
@app.post('/post/',status_code=201)
async def createpost(post: Post):
    try:
        print(post,'---------')
        
        cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *", (post.title, post.content))
        conn.commit()
        post=cursor.fetchone()
        print(post,'---------')
        conn.commit()

        cursor.execute("SELECT * FROM posts")
        posts = cursor.fetchall()


        return {"DATA":'teststst',"status":200,'message':'success','dataa':posts} 
    except Exception as e:
        print(e)
        return {"DATA":'teststst',"status":500,'message':'error','dataa':e}




@app.get('/post/{id}')
async def get_post(id: int, response: Response):
    print(id,'---------')

    try:
        cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
        post = cursor.fetchone()
        print(post,'---------')
        if post is None:
            raise HTTPException(status_code=404, detail="Item not found")
        return {"DATA":'teststst',"status":200,'message':'success','data':post}
    except Exception as e:
        print(e)
        return {"DATA":'teststst',"status":500,'message':'error','dataa':e}   




def find_post(id):
    for p in dummy_posts:
        if p['id'] == id:
            print("found",p)
            return p
    print("not found Sorry")
    return None



@app.get('/posts/latest')
def get_latest_posts():
    latest_posts = dummy_posts[-1:-4:-1]
    return {"DATA":'teststst',"status":200,'message':'success','data':latest_posts}




@app.delete('/post/{id}',status_code=204)
def delete_post(id: int):
    print(id,'---------')
    try:
        cursor.execute("DELETE FROM posts WHERE id = %s returning *", (id,))
        deleted_post = cursor.fetchone()
        print(deleted_post,'---------')
        conn.commit()

        if deleted_post is None:
            raise HTTPException(status_code=404, detail="Item not found")
            
        return {"DATA":'teststst',"status":200,'message':'success','data':deleted_post}
    except Exception as e:
        print("ERROR== :",e)
        raise HTTPException(status_code=404, detail="Item not found")




@app.put('/post/{id}')
def update_post(id: int, post: Post):
    print(id,'---------')
    
    try:
        cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s returning *", (post.title, post.content, id)) 
        conn.commit()
        post=cursor.fetchone()
        print(post,'---------')
        if post is None:
            raise HTTPException(status_code=404, detail="Item not found")
            
        return {"DATA":'teststst',"status":200,'message':'success','data':post}
    except Exception as e:
        print(e)
        return {"DATA":'teststst',"status":500,'message':'error','dataa':e}






# @app.put('/post/{id}')
# def update_post(id: int, post: Post):
#     print(id,'---------')
#     # post=post.dict()
#     posst = find_post(id)
#     if posst is None:
#         raise HTTPException(status_code=404, detail="Item not found")
    
#     posst['title'] = post.title
#     posst['content'] = post.content
#     posst['age'] = post.age
#     posst['time'] = post.time
#     posst['opt'] = post.opt
#     return {"DATA":'teststst',"status":200,'message':'success','data':posst}

