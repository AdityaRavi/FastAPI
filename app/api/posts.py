from pydantic.types import UUID4
from app.db import db
from .base import BaseAPI

class PostsAPI(BaseAPI):
  def get_all(self):
    return db.execute("""SELECT * from posts""")

  def get_by_id(self, id: UUID4):
    return db.execute("""SELECT * from posts WHERE id=%s""", (str(id), ))

  def create(self, title: str, content: str):
    return  db.execute("""INSERT INTO posts (title, content) VALUES (%s, %s) RETURNING *""", (title, content))

  def update_by_id(self, id: UUID4, title: str, content: str):
    return db.execute("""UPDATE posts SET title=%s, content=%s WHERE id=%s RETURNING *""", (title, content, str(id)))

  def delete_by_id(self, id: UUID4):
    return db.execute("""DELETE FROM posts WHERE ID=%s RETURNING *""", (str(id), ))