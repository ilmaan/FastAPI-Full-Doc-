from fastapi import FastAPI
from fastapi.params import Body

from pydantic import BaseModel
from typing import Optional

from random import randrange



app = FastAPI()



class Post(BaseModel):
    title: str
    content: str
    age: int
    time: str = None
    opt: Optional[int] = None






dummy_posts = [
         {"id":1,"title": "title1", "content": "content1", "age": 1, "time": "time1"},
         {"id":2,"title": "title2", "content": "content2", "age": 2, "time": "time2"},
         {"id":3,"title": "title3", "content": "content3", "age": 3, "time": "time3"}]


@app.get("/")
async def root():
    return {"message": "Hello Worldss"}


@app.get('/post/')
async def payload(payload: dict=Body(None)):
    print(payload,'---------')
    # return {"DATA":'teststst',"status":200,'message':'success','data':payload.get('time')}
    return {"posts":dummy_posts}




@app.post('/post/')
async def createpost(post: Post):
    print(post,'---------')
    post=post.dict()
    post['id']=randrange(1,100)
    dummy_posts.append(post)


    return {"DATA":'teststst',"status":200,'message':'success','dataa':dummy_posts}


@app.get('/post/{id}')
async def get_post(id: int):
    print(id,'---------')
    return {"DATA":'teststst',"status":200,'message':'success','data':dummy_posts[id]}
