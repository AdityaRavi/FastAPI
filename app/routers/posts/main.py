from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic.types import UUID4
from starlette import status

from app.api.posts import PostsAPI
from app.routers.posts.schemas import PostOut, PostIn

router = APIRouter(prefix='/posts', tags=['Posts'])

@router.get('', response_model=PostOut)
def get_all_posts(api: PostsAPI = Depends()):
  rows = api.get_all()

  return {"rows": rows}

@router.get('/{id}', response_model=PostOut)
def get_post(id: UUID4, api: PostsAPI = Depends()):
  rows = api.get_by_id(id)

  if not rows:
    raise HTTPException(status_code=404, detail=f"Post with id={id} does not exist")

  return {"rows": rows}

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PostOut)
def create_post(post: PostIn, api: PostsAPI = Depends()):
    rows = api.create(post.title, post.content)

    return {"rows": rows}

@router.put('/{id}', status_code=status.HTTP_205_RESET_CONTENT, response_model=PostOut)
def update_post(id: UUID4, updated_post_content: PostIn, api: PostsAPI = Depends()):
    rows = api.update_by_id(id, updated_post_content.title, updated_post_content.content)

    if not rows:
        raise HTTPException(
            status_code=404,
            detail=f"Update failed. Post with id={id} does not exist.")

    return {"rows": rows}

@router.delete('/{id}', response_model=PostOut)
def delete_post(id: UUID4, api: PostsAPI = Depends()):
    rows = api.delete_by_id(id)

    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Delete failed. Post with id={id} does not exist.")

    return {"rows": rows}

