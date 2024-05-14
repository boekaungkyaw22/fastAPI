from typing import Optional
from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()
class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None

my_post = [{"title" : "title of post 1", "content" : "content of post 1", "id" : 1},{"title" : "title of post 2", "content" : "content of post 2", "id" : 2}]

def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p
        
def find_index_of_post(id):
    for i, p in enumerate(my_post):
        if p["id"] == id:
            return i

@app.get("/")
async def root():
    return {"Hello": "World"} 

@app.get("/post")
def get_posts() : 
    return {"data" : my_post }

@app.post("/posts",status_code= status.HTTP_201_CREATED)
async def create_posts(new_post :Post):
    post_dict = new_post.model_dump();
    post_dict["id"] = randrange(0, 1000000)
    my_post.append(post_dict)
    return {"date" : post_dict}  

@app.get("/posts/{id}")
async def get_post(id : int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found.")
    return {"post_detail" : post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id : int, response: Response):
    index  = find_index_of_post(id);
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} was not found.")
    my_post.pop(index);
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id :int, post: Post):
    index = find_index_of_post(id);
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id : {id} was not found")
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_post[index] = post_dict
    return {"message": post_dict}

 