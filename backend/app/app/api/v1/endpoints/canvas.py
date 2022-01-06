from app import crud, schemas
from app.api.dependencies import get_canvas, get_db
from fastapi import APIRouter, Depends, HTTPException, Path, status
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session

router = APIRouter()


@router.get("/", summary="Returns a list of all created canvases")
def get_all_canvases(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    canvases = crud.canvas.get_multi(db, skip=skip, limit=limit)
    return canvases


@router.post(
    "/",
    summary="Creates the celery canvas function and stores it in the database",
    status_code=status.HTTP_201_CREATED,
)
def create_canvas(canvas: schemas.CanvasCreate, db: Session = Depends(get_db)):
    try:
        return crud.canvas.create(db, obj_in=canvas)
    except IntegrityError as err:
        if type(err.orig) is UniqueViolation:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Canvas {canvas.name} already exists",
            )
        else:
            raise err


@router.get("/{canvas_name}", summary="Returns the specific canvas")
def get_canvas_by_name(canvas: schemas.Canvas = Depends(get_canvas)):
    return canvas


@router.patch(
    "/{canvas_name}",
    summary="Edits the celery canvas metadata",
)
def edit_canvas(
    updated_canvas: schemas.CanvasUpdate,
    canvas_name: str = Path(..., title="Name of the canvas to delete"),
    db: Session = Depends(get_db),
):
    # TODO: Create
    #       crud.canvas.update_by_name(db=db, name=canvas_name, obj_in=updated_canvas)
    ...


@router.delete(
    "/{canvas_name}",
    summary="Removes canvas from backend store",
)
def delete_canvas(
    canvas_name: str = Path(..., title="Name of the canvas to delete"),
    db: Session = Depends(get_db),
):
    if canvas := crud.canvas.remove_by_name(db, name=canvas_name):
        return canvas
    else:
        raise HTTPException(status_code=404, detail=f"Canvas '{canvas_name}' not found")
