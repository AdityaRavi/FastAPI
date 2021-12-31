from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from pydantic.types import UUID4
from app.db import DB

app = FastAPI()
db = DB()


class Post(BaseModel):
    title: str
    content: str


@app.get('/')
def root():
    return {"message": "Hello World!"}


@app.get('/posts')
def get_posts():
    results = db.execute("""SELECT * FROM posts""")
    return {"data": results}


@app.get('/posts/{id}')
def get_post(id: UUID4):
    post = db.execute("""SELECT * from posts WHERE id=%s""", (str(id), ))
    print(post)
    print(type(post))
    if not post:
        raise HTTPException(status_code=404,
                            detail=f"Post with id={id} not found.")

    return {"data": post}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post = db.execute(
        """INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *""",
        (post.title, post.content))

    return {"detail": post}


@app.put('/posts/{id}', status_code=status.HTTP_205_RESET_CONTENT)
def update_post(id: UUID4, updated_post_content: Post):
    updated_post = db.execute(
        """
        UPDATE posts
        SET title=%s, content=%s
        WHERE id=%s
        RETURNING *
    """, (updated_post_content.title, updated_post_content.content, str(id)))

    if not updated_post:
        raise HTTPException(
            status_code=404,
            detail=f"Update failed. Post with id={id} does not exist.")

    return {"detail": updated_post}


@app.delete('/posts/{id}')
def delete_post(id: UUID4):
    deleted_post = db.execute(
        """
        DELETE FROM posts
        WHERE id=%s
        RETURNING *
    """, (str(id), ))

    print(deleted_post)
    print(type(deleted_post))
    if not deleted_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Delete failed. Post with id={id} does not exist.")

    return {
        "detail": f"Success! Post with id={id} was deleted.",
        "data": deleted_post
    }
