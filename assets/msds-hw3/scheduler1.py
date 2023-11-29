# Script (with AsyncIOScheduler):

from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import aiohttp
from asyncio import Semaphore
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configurable variables
max_requests = 10 # limit the number of concurrent requests to the FastAPI server at any given time.

request_interval = 3  # seconds
number_of_trips = 30

sem = Semaphore(max_requests)

async def make_request(session):
    async with sem:
        # Define the payload for the number of trips to generate
        payload = {"number_of_trips": number_of_trips}

        try:
            # Make the POST request to the new endpoint
            async with session.post("http://localhost:8001/api/generate-multiple-trips", json=payload) as response:
                if response.status == 200:
                    response_json = await response.json()
                    logging.info("Request successful: %s", response_json)
                else:
                    logging.error("Request failed with status %s", response.status)
        except Exception as e:
            logging.exception("An error occurred during request: %s", e)

async def trigger_multiple_trip_generation():
    async with aiohttp.ClientSession() as session:
        while True:
            await make_request(session)
            # Removed asyncio.sleep, as the scheduler handles the interval
            # await asyncio.sleep(request_interval)

if __name__ == "__main__":
    scheduler = AsyncIOScheduler()
    scheduler.add_job(trigger_multiple_trip_generation, 'interval', seconds=request_interval)
    scheduler.start()

    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        logging.info("Scheduler terminated.")
        scheduler.shutdown()
        asyncio.get_event_loop().close()
