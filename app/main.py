from fastapi import FastAPI
from app.db import db
from app.routers.posts.main import router as postsRouter

app = FastAPI()
app.include_router(postsRouter)

@app.on_event('startup')
def setup():
    db.connect_pool()

@app.on_event('shutdown')
def shutdown():
    db.close_pool()

@app.get('/')
def root():
    return {"message": "Hello World!"}
