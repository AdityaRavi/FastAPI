from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()
posts = []  #store locally for now


class Post(BaseModel):
    title: str
    content: str


def find_post_by_id(id: int):
    for idx, post in enumerate(posts):
        if post['id'] == id:
            return post, idx
    return (None, None)


@app.get('/')
def root():
    return {"message": "Hello World!"}


@app.get('/posts')
def get_posts():
    return {"data": posts}


@app.get('/posts/{id}')
def get_post(id: int):
    print(id)
    (post, _) = find_post_by_id(id)

    if not post:
        raise HTTPException(status_code=404,
                            detail=f"Post with id={id} not found.")

    return {"data": post}


@app.post('/posts/{id}', status_code=status.HTTP_201_CREATED)
def create_post(id: int, post: Post):
    (existing_post, _) = find_post_by_id(id)
    if existing_post:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Create failed. Post with id={id} already exists.")

    new_post = dict(post.dict(), id=id)
    posts.append(new_post)

    return {"detail": f"Success! Post with id={id} was successfully created."}


@app.put('/posts/{id}', status_code=status.HTTP_205_RESET_CONTENT)
def update_post(id: int, updated_post: Post):
    (existing_post, existing_post_idx) = find_post_by_id(id)

    if not existing_post:
        raise HTTPException(
            status_code=404,
            detail=f"Update failed. Post with id={id} does not exist.")

    posts[existing_post_idx] = dict(updated_post.dict(), id=id)

    return {"detail": f"Success! Post with id={id} was updated."}


@app.delete('/posts/{id}')
def delete_post(id: int):
    (post, idx) = find_post_by_id(id)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Delete failed. Post with id={id} does not exist.")

    posts.pop(idx)
    return {"detail": f"Success! Post with id={id} was deleted."}
