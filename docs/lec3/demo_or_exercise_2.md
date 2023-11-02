# Demo #3B: Producer and Consumer with Kafka with FastAPI


Now, I want to have a input to specify the position of the players. For example, I want to create 5 goalkeepers, rather than 5 random players.  How would I achieve that?

Here's what you need to modify in your previous code to achieve this:

1. **Modify the Command Class**:
   Update the `CreatePeopleCommand` class in your `commands.py` to include a field for the player's position. If you don't have a way to specify the position in the current structure, this is the step you'll need to take.

      ```python
      # commands.py
      from pydantic import BaseModel

      class CreatePeopleCommand(BaseModel):
         count: int
         position: str
      ```

2. **Update the API Endpoint**:
   Modify the `create_soccer_players` function in `main.py` to use the specified position instead of randomly selecting one.

      ```python
      # main.py
      @app.post('/api/soccer_players', status_code=201, response_model=List[SoccerPlayer])
      async def create_soccer_players(cmd: CreatePeopleCommand):
         ...
         # Remove the positions list, as you'll use the position from the cmd parameter
         # positions = ["Forward", "Midfielder", "Defender", "Goalkeeper"]

         # Generate random soccer player data based on the given count.
         for _ in range(cmd.count):
            soccer_player = SoccerPlayer(
                  id=str(uuid.uuid4()), 
                  name=faker.name(), 
                  position=cmd.position,  # Use the specified position.
                  speed=random.randint(0, 10),
                  stamina=random.randint(0, 10),
                  strength=random.randint(0, 10),
                  technique=random.randint(0, 10)
            )
            ...
      ```

3. **Position Validation (Optional but Recommended)**:
   You might want to validate the incoming position to ensure it's one of the expected values. Add this check at the beginning of the `create_soccer_players` function:

      ```python
      valid_positions = ["Forward", "Midfielder", "Defender", "Goalkeeper"]
      if cmd.position not in valid_positions:
         raise ValueError(f"Invalid position: {cmd.position}. Expected one of {valid_positions}.")
      ```

With these changes, you can now specify the position of the players you want to create. When you make a request to your API, you can now send both the count and the position as part of the request body, like so:

```json
{
    "count": 5,
    "position": "Goalkeeper"
}
```

This request would create 5 goalkeepers. Adjust the "position" value as needed for different positions.

**Scripts used in the demo**

- [main.py](../assets/msds-demo3-additional/main.py)
- [commands.py](../assets/msds-demo3-additional/commands.py)
- [entities.py (unchanged)](../assets/msds-demo3-additional/entities.py)
- [requirements.txt (unchanged)](../assets/msds-demo3-additional/requirements.txt)
- [config.ini (unchanged)](../assets/msds-demo3-additional/config.ini)
- [consumer.py (unchanged)](../assets/msds-demo3-additional/consumer.py)