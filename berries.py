from fastapi import FastAPI
from fastapi.responses import Response
from poke_berries.api import router
import utils.logger  # noqa
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get('/')
async def home():
    logger.info("We are logging stuff in json format my friend.")
    return Response("Hello from Poke Berry App")


app.include_router(router)


