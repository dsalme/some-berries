import asyncio
import base64
import io
import statistics
import os
import httpx
import matplotlib.pyplot as plt
from fastapi.exceptions import HTTPException
from cachetools import TTLCache
from collections import Counter
from berries_client import client

import logging


logger = logging.getLogger(__name__)

CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", 60))
cache = TTLCache(1, CACHE_TTL_SECONDS)

def calculate_berry_stats(growth_times):

    min_gt = min(growth_times)
    max_gt = max(growth_times)
    median_gt = round(statistics.median(growth_times), 2)
    variance_gt = round(statistics.variance(growth_times), 2)
    mean_gt = round(statistics.mean(growth_times), 2)
    frequency = Counter(growth_times)

    return {
        "min_growth_time": min_gt,
        "median_growth_time": median_gt, 
        "max_growth_time": max_gt,
        "variance_growth_time": variance_gt,
        "mean_growth_time": mean_gt,
        "frequency_growth_time": frequency
    }

def generate_plot(berries_data):
    growth_times = berries_data.get("growth_times")
    fig, axs = plt.subplots(tight_layout=True)

    axs.set_title("Growth time histogram")
    axs.set_xlabel("Count")
    axs.set_ylabel("Growth time")
    axs.hist(growth_times, bins=max(growth_times))

    img = io.BytesIO()
    fig.savefig(img, format='png',
                bbox_inches='tight')

    b64string = "data:image/png;base64,"
    b64string += base64.b64encode(img.getvalue()).decode('utf8')

    return b64string


async def get_berries_data():
    if not cache.get("berries_data"):
        logger.info("Cache key not found, building cache.")
        berries_data = await client.get_berries_data()

        to_json = berries_data.json()
        count = to_json.get("count")

        tasks = set()
        for i in range(1, count+1):
            task = asyncio.create_task(client.get_berry(id=i))
            tasks.add(task)
            task.add_done_callback(tasks.discard)

        results = await asyncio.gather(*tasks)

        names = []
        growth_times = []
        for berry_resp in results:
            berry = berry_resp.json()
            names.append(berry.get("name"))
            growth_times.append(berry.get("growth_time"))

        cache["berries_data"] = {
            "names": names,
            "growth_times": growth_times
        }

        return cache.get("berries_data")
    else:
        logger.info("Found berries cache!")
        return cache.get("berries_data")

async def get_berry_stats():
    try:
        berries_data = await get_berries_data()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=404)
    else:
        response_dict = {
            "names": berries_data.get("names"),
            **calculate_berry_stats(berries_data.get("growth_times"))
        }
        return response_dict

async def get_data_and_plot():
    try:
        berries_data = await get_berries_data()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=404)
    else:
        b64plot = generate_plot(berries_data)
        response_dict = {
            "img": b64plot,
            "berries_data": berries_data
        }
        return response_dict
