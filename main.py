from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

# instance of fast api

app = FastAPI()


# class for post
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


my_posts = [{"title": "title of the post", "content": "content of post 1", "id": 1}]


@app.get("/")
async def root():
    return {"message": "Hello World hope you are good"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# title should be string content => should be string

@app.post("/posts")
def create_posts(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0, 500)
    my_posts.append(post_dict)
    return {"new post": post_dict}
