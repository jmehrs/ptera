from sqlalchemy.orm import Session

from app import crud, models
from app.schemas import CanvasCreate, TaskSignature
from .utils import random_lower_string
from .task import random_signature


def create_random_canvas(db: Session) -> models.Canvas:
    name = random_lower_string()
    canvas = TaskSignature.from_signature(random_signature())
    obj_in = CanvasCreate(name=name, canvas=canvas)
    return crud.canvas.create(db=db, obj_in=obj_in)
