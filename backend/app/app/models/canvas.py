from celery import signature as celery_signature
from celery.canvas import Signature
from sqlalchemy import Column, Integer, String
from app.models.model_base import Base, JSONBType


class Canvas(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    canvas = Column(JSONBType)

    @property
    def signature(self) -> Signature:
        return celery_signature(self.canvas)
