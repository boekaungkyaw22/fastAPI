from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()

@app.get("/")
async def root():
    return {"Hello": "World"} 

@app.get("/post")
def get_posts() : 
    return {"data" : "This is your posts"}

@app.post("/createposts")
async def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"Created Payload" : f"{payload["title"]} , {payload["description"]}"}