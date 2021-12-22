from sqlalchemy.orm import Session

from app import crud
from app.schemas import CanvasCreate, CanvasUpdate, TaskSignature
from app.tests.utils.canvas import create_random_canvas
from app.tests.utils.task import random_signature
from app.tests.utils.utils import random_lower_string


def test_create_canvas(db: Session) -> None:
    name = random_lower_string()
    sig = TaskSignature.from_signature(random_signature())
    obj_in = CanvasCreate(name=name, canvas=sig)
    canvas = crud.canvas.create(db=db, obj_in=obj_in)

    assert canvas.name == name
    assert canvas.canvas == sig.dict()


def test_get_canvas(db: Session) -> None:
    canvas = create_random_canvas(db)
    stored_canvas = crud.canvas.get(db=db, id=canvas.id)

    assert stored_canvas
    assert canvas.name == stored_canvas.name
    assert canvas.canvas == stored_canvas.canvas


def test_update_canvas(db: Session) -> None:
    canvas = create_random_canvas(db)

    sig2 = TaskSignature.from_signature(random_signature())
    canvas_update = CanvasUpdate(canvas=sig2)
    canvas2 = crud.canvas.update(db=db, db_obj=canvas, obj_in=canvas_update)

    assert canvas.id == canvas2.id
    assert canvas.name == canvas2.name
    assert canvas2.canvas == sig2


def test_remove_canvas(db: Session) -> None:
    canvas = create_random_canvas(db)
    removed_canvas = crud.canvas.remove(db=db, id=canvas.id)
    invalid_canvas = crud.canvas.get(db=db, id=canvas.id)

    assert invalid_canvas is None
    assert removed_canvas.id == canvas.id
    assert removed_canvas.name == canvas.name
    assert removed_canvas.canvas == canvas.canvas
