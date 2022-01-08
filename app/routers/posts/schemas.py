from typing import List, Tuple
from pydantic.main import BaseModel
from pydantic.types import UUID4
from datetime import datetime


class PostIn(BaseModel):
  title: str
  content: str

class PostOut(BaseModel):
  rows: List[Tuple[UUID4, str, str, datetime]]