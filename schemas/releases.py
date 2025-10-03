from pydantic import BaseModel
from typing import Optional

class ReleaseCreate(BaseModel):
    tag_name: str
    name: str
    body: Optional[str] = ""

class ReleaseUpdate(BaseModel):
    name: Optional[str] = None
    body: Optional[str] = None
