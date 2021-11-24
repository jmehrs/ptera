from typing import Any, Dict, Optional, Union
from fastapi.encoders import jsonable_encoder

from sqlalchemy.orm import Session

from app.crud.crud_base import CRUDBase
from app.models.canvas import Canvas
from app.schemas.canvas import CanvasCreate, CanvasUpdate


class CRUDCanvas(CRUDBase[Canvas, CanvasCreate, CanvasUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Canvas]:
        return db.query(Canvas).filter(Canvas.name == name).first()

    def update(
        self,
        db: Session,
        *,
        db_obj: Canvas,
        obj_in: Union[CanvasUpdate, Dict[str, Any]]
    ) -> Canvas:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        return super().update(db, db_obj=db_obj, obj_in=update_data)


canvas = CRUDCanvas(Canvas)