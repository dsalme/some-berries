from fastapi.requests import Request
import httpx
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates

from poke_berries.serializers import BerryStats
from poke_berries.berries import get_berry_stats, get_data_and_plot
import logging


logger = logging.getLogger(__name__)

templates = Jinja2Templates(directory="templates")
router = APIRouter(prefix="")

@router.get("/allBerryStats", response_model=BerryStats)
async def berry_stats():
    try:
        poke_stats = await get_berry_stats()
    except httpx.RequestError as e:
        logger.warning(e)
        raise e
    else:
        logger.info("We also log some berry-related things")
        return JSONResponse(poke_stats)


@router.get("/berriesGraph")
async def berries_plot(request: Request):
    plot_view_data = await get_data_and_plot()

    return templates.TemplateResponse(
        request=request, name="plot_page.html", context=plot_view_data
    )
        #return JSONResponse(poke_stats)
