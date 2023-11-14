# Script (without scheduler):

#########################################################
#                                                       #
#  DON'T CHANGE ANYTHING HERE IN THIS SCRIPT            #
#                                                       #
#########################################################

import asyncio
import aiohttp
from asyncio import Semaphore
import logging

# Configurable variables
max_requests = 10 # limit the number of concurrent requests to the FastAPI server at any given time.

request_interval = 0.1  # seconds
number_of_trips = 3
# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
            logging.info("Triggering trip generation")
            await make_request(session)
            logging.info("Waiting for next interval")
            await asyncio.sleep(request_interval)

if __name__ == "__main__":
    try:
        logging.info("Starting trip generation scheduler")
        asyncio.run(trigger_multiple_trip_generation())  # This handles the loop
    except KeyboardInterrupt:
        logging.info("Script terminated by user.")
    except Exception as e:
        logging.exception("An unexpected error occurred: %s", e)
    finally:
        logging.info("Scheduler stopped")
