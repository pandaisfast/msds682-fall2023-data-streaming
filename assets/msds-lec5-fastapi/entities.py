# entities.py

# This module defines the SoccerPlayer model using Pydantic for data validation and settings management.
# Each SoccerPlayer instance represents a soccer player with unique attributes such as ID, name, position,
# and ratings for speed, stamina, strength, and technique.

from pydantic import BaseModel

# Represents a soccer player with specific attributes.
class SoccerPlayer(BaseModel):
    id: str  # Unique identifier for the soccer player
    name: str  # Name of the soccer player
    position: str  # Playing position (e.g., Forward, Midfielder)
    speed: int  # Speed rating (0-10)
    stamina: int  # Stamina rating (0-10)
    strength: int  # Strength rating (0-10)
    technique: int  # Technique rating (0-10)
