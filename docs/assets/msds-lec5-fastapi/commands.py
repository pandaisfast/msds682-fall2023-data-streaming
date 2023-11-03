# commands.py         
# Defines the data format of API requests (Request Body). Pydantic model for API request and response
from pydantic import BaseModel

class CreatePeopleCommand(BaseModel):
    count: int
    position: str
