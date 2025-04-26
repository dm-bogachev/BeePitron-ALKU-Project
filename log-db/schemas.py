from pydantic import BaseModel
from typing import Optional

class LogEntryCreate(BaseModel):
    title: str
    description: Optional[str] = None
    # add additional fields as needed

    class Config:
        orm_mode = True