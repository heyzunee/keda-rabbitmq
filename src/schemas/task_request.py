from datetime import datetime

from pydantic import BaseModel


class Request(BaseModel):
    request_id: str
    request: str
    created_at: datetime
