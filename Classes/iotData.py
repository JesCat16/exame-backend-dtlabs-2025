from pydantic import BaseModel
import datetime

class Data(BaseModel):
    server_ulid: str
    timestamp: datetime
    temperature: float
    humidity: float
    voltage: float
    current: float