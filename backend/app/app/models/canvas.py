from celery import schedules, signature as signature_
from celery.canvas import Signature
from sqlalchemy import Column, Integer, String
from app.models.model_base import Base, JSONBType
import json


class Canvas(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    canvas = Column(JSONBType)

    @property
    def signature(self) -> Signature:
        json_signature = json.loads(self.canvas)
        return signature_(json_signature)
