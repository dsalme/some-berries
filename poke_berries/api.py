import httpx
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from poke_berries.berries import get_berry_stats
import logging


logger = logging.getLogger(__name__)


router = APIRouter(prefix="")

@router.get("/allBerryStats")
async def berry_stats():
    logger.info("We also log some berry-related things")
    try:
        poke_stats = await get_berry_stats()
    except httpx.RequestError as e:
        logger.warning(e)
        raise e
    else:
        return JSONResponse(poke_stats)
