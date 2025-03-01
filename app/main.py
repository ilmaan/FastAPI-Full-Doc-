
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body

from pydantic import BaseModel
from typing import Optional, List

from random import randrange


import psycopg2
# from psycopg2 import Error, RealDictCursor

import time
from datetime import datetime

from . import models, schemas
from . import database
from .database import SessionLocal, engine, get_db
from sqlalchemy.orm import Session
from fastapi import Depends




models.Base.metadata.create_all(bind=engine)  

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
    published: bool = True
    created_at: Optional[datetime] = None
    






dummy_posts = [
         {"id":1,"title": "title1", "content": "content1", "age": 1, "time": "time1"},
         {"id":2,"title": "title2", "content": "content2", "age": 2, "time": "time2"},
         {"id":3,"title": "title3", "content": "content3", "age": 3, "time": "time3"}]




@app.get('/sqlalchemy')
async def sqlalchemy(db: Session = Depends(get_db)):
    posts = db.query(models.NewPost).all()
    print(posts)

    return {"message": "Hello World-------ss","posts":posts}



@app.get("/")
async def root():
    return {"message": "Hello Worldss"}


@app.get('/post/',response_model=List[schemas.PostOut])
async def payload(db: Session = Depends(get_db)):
    try:
        # print(payload,'---------')
        # return {"DATA":'teststst',"status":200,'message':'success','data':payload.get('time')}

        # cursor.execute("SELECT * FROM posts")
        # posts = cursor.fetchall()

        posts = db.query(models.NewPost).all()
        
        print(posts,'---------')

        # return {"posts":posts}
        return posts
    except Exception as e:
        print("ERROR")
        # print("error------->>>> ",e)
        # return {"posts":e}




# USING DATABASE POST
@app.post('/post/',status_code=201,response_model=schemas.PostOut)
async def createpost(post: schemas.Post,db: Session = Depends(get_db)):
    try:
        print(post,'---------')
        
        # cursor.execute("INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *", (post.title, post.content))
        # conn.commit()
        # post=cursor.fetchone()
        # print(post,'---------')
        # conn.commit()

        

        # new_post = models.NewPost(title=post.title, content=post.content,published=True)
        new_post = models.NewPost(**post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        # return {"DATA":'teststst',"status":200,'message':'success','dataa':new_post}
        return new_post


        # cursor.execute("SELECT * FROM posts")
        # posts = cursor.fetchall()


        # return {"DATA":'teststst',"status":200,'message':'success','dataa':posts} 
    except Exception as e:
        print(e)
        return {"DATA":'teststst',"status":500,'message':'error','dataa':e}




@app.get('/post/{id}',response_model=schemas.PostOut)
async def get_post(id: int, response: Response,db: Session = Depends(get_db)):
    print(id,'---------')

    try:
        post = db.query(models.NewPost).filter(models.NewPost.id == id).first()
        print(post,'---------')
        
        # cursor.execute("SELECT * FROM posts WHERE id = %s", (id,))
        # post = cursor.fetchone()
        # print(post,'---------')
        if post is None:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # return {"DATA":'teststst',"status":200,'message':'success','data':post}
        return post
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



@app.get('/posts/latest',response_model=schemas.PostOut)
def get_latest_posts(db: Session = Depends(get_db)):
    # latest_posts = dummy_posts[-1:-4:-1]
    try:
        latest_posts = db.query(models.NewPost).order_by(models.NewPost.created_at.desc()).limit(10).all()
    # return {"DATA":'teststst',"status":200,'message':'success','data':latest_posts}
        return latest_posts
    except Exception as e:
        print('error---\n\n\n\n\---->>>> ',e)




@app.delete('/post/{id}', status_code=204)
def delete_post(id: int,db: Session = Depends(get_db)):
    print(id,'---------')
    try:
        deleted_post = db.query(models.NewPost).filter(models.NewPost.id == id)
        print(deleted_post,'---------',"deleted_post-----------") 

        if deleted_post.first() is None:  # Check if the post exists
            raise HTTPException(status_code=404, detail="Item not found")

        deleted_post.delete(synchronize_session=False)
        db.commit()
        # db.refresh(deleted_post)


        
        # cursor.execute("DELETE FROM posts WHERE id = %s returning *", (id,))
        # deleted_post = cursor.fetchone()
        # print(deleted_post,'---------')
        # conn.commit()

        # if deleted_post is None:
        #     print("deleted_post is None")
        #     raise HTTPException(status_code=404, detail="Item not found")
            
        return {"DATA":'teststst',"status":204,'message':'successfully deeted','id':id}
    except Exception as e:
        print("ERROR== :",e)
        raise HTTPException(status_code=404, detail="Item not found")




@app.put('/post/{id}',response_model=schemas.PostOut)
def update_post(id: int, update_post: schemas.Post,db: Session = Depends(get_db)):
    print(id,'---------')
    
    try:
        post = db.query(models.NewPost).filter(models.NewPost.id == id).first()
        print(post,'---------')
        if post is None:
            raise HTTPException(status_code=404, detail="Item not found")
        
        # Update the attributes of the post object directly
        for key, value in update_post.dict().items():
            setattr(post, key, value)



        db.commit()
        
        
        # cursor.execute("UPDATE posts SET title = %s, content = %s WHERE id = %s returning *", (post.title, post.content, id)) 
        # conn.commit()
        # post=cursor.fetchone()
        print(post,'---------')
        if post is None:
            raise HTTPException(status_code=404, detail="Item not found")
            
        # return {"DATA":'teststst',"status":200,'message':'success','data':post}
        return post
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

