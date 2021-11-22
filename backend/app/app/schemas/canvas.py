from typing import Optional
from pydantic.main import BaseModel
from .task import TaskSignature


# Shared properties
class CanvasBase(BaseModel):
    name: Optional[str] = None
    canvas: Optional[TaskSignature] = None


# Properties to receive via API on creation
class CanvasCreate(CanvasBase):
    name: str
    canvas: TaskSignature


# Properties to receive via API on update
class CanvasUpdate(CanvasBase):
    pass


class CanvasInDBBase(CanvasBase):
    id: Optional[int] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Canvas(CanvasInDBBase):
    pass
