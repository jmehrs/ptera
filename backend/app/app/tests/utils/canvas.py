from app import crud, models
from app.schemas import CanvasCreate, TaskSignature
from sqlalchemy.orm import Session

from .task import (
    bad_malformed_task,
    bad_unregistered_task,
    good_bare_minimum_task,
    good_complex_task,
    random_signature,
)
from .utils import random_int, random_lower_string

good_bare_minimum_canvas = {
    "name": f"Basic Canvas {random_int()}",
    "canvas": good_bare_minimum_task,
}

good_complex_canvas = {
    "name": f"Complex Canvas {random_int()}",
    "canvas": good_complex_task,
}

bad_unregistered_canvas = {
    "name": f"Unregistered Canvas {random_int()}",
    "canvas": bad_unregistered_task,
}

bad_malformed_canvas = {
    "name": f"Malformed Canvas {random_int()}",
    "canvas": bad_malformed_task,
}


def create_random_canvas(db: Session) -> models.Canvas:
    name = random_lower_string()
    canvas = TaskSignature.from_signature(random_signature())
    obj_in = CanvasCreate(name=name, canvas=canvas)
    return crud.canvas.create(db=db, obj_in=obj_in)


def create_test_canvas(db: Session) -> models.Canvas:
    canvas = TaskSignature(task="test.ping")
    obj_in = CanvasCreate(name=f"Test Ping {random_int()}", canvas=canvas)
    return crud.canvas.create(db=db, obj_in=obj_in)
