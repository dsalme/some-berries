from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
import httpx
from berries_client import client
import logging

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/allBerryStats")

@router.get("/")
async def berry_stats():
    logger.info("We also log some berry-related things")
    try:
        poke_things = await client.get_berries()
    except httpx.RequestError as e:
        logger.warning(e)
        raise e
    else:
        logger.info(poke_things)

        resp = poke_things.json()
        return JSONResponse(resp)

