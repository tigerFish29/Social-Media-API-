from fastapi import FastAPI, Response, status, HTTPException
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


# find the posts [id]
def find_posts(id):
    for post in my_posts:
        if post["id"] == id:
            return post


# get the index of a post
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
async def root():
    return {"message": "Hello World hope you are good"}


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


# title should be string content => should be string

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id'] = randrange(0, 500)
    my_posts.append(post_dict)
    return {"new post": post_dict}


# get a post
@app.get("/post/{id}")
def get_post(id: int, response: Response):
    post = find_posts(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"post_detail": post}


# delete a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item does not exit!")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update the post
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"message": "updated schemas"}


