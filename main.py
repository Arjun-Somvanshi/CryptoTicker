import FastAPI
from typing import Union
from pydantic import BaseModel

app = FastAPI()

class Alert(BaseModel):
    status: str = "created"
    targetPrice: float

