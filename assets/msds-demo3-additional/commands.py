# commands.py
from pydantic import BaseModel

class CreatePeopleCommand(BaseModel):
    count: int
    position: str
