from fastapi import FastAPI, Response, status
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


# @app.get('/post/{id}')
# async def get_post(id: int):
#     print(id,'---------')
#     return {"DATA":'teststst',"status":200,'message':'success','data':dummy_posts[id]}


@app.get('/post/{id}')
async def get_post(id: int, response: Response):
    print(id,'---------')

    try:
        post=find_post(id)
        if post is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return {"DATA":'UNDEFINED',"status":404,'message':'not found','data':"SORRY NOT FOUND"} 
            
        return {"DATA":'teststst',"status":200,'message':'success','data':post}
    except Exception as e:
        print('ERROR== :',e)
        return {"DATA":'teststst',"status":500,'message':'error','data':None}



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