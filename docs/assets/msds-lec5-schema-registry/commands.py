# commands.py         
# Defines the data format of API requests (Request Body)
from pydantic import BaseModel

class CreatePeopleCommand(BaseModel):
    count: int
    position: str
