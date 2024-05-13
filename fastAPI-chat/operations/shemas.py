from pydantic import BaseModel
from datetime import datetime


class OperationCreate(BaseModel):
    id: int
    instrument: str
    type: str
    datetime: datetime
    quantity: float
    pair: str
