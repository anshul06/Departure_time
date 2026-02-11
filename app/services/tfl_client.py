import httpx
from app.config import TFL_API_KEY, TFL_BASE_URL
from app.logger import logger


async def get_nearby_stop_points(lat: float, lon: float, radius: int = 800):
    logger.info(f"Fetching nearby stop points for lat={lat}, lon={lon}")

    url = f"{TFL_BASE_URL}/StopPoint"
    params = {
        "lat": lat,
        "lon": lon,
        "radius": radius,
        "stopTypes": "NaptanMetroStation,NaptanPublicBusCoachTram",
        "app_key": TFL_API_KEY,
    }

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if "stopPoints" not in data:
                logger.warning("Response missing 'stopPoints' key, returning empty list")
                return []
            
            logger.info("Successfully fetched stop points")
            return data["stopPoints"]
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error fetching stop points: {e.response.status_code} - {e.response.text}")
        raise
    except httpx.RequestError as e:
        logger.error(f"Request error fetching stop points: {e}")
        raise


async def get_arrivals(stop_point_id: str):
    logger.info(f"Fetching arrivals for stop_point_id={stop_point_id}")

    url = f"{TFL_BASE_URL}/StopPoint/{stop_point_id}/Arrivals"
    params = {"app_key": TFL_API_KEY}

    try:
        async with httpx.AsyncClient(timeout=5) as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not isinstance(data, list):
                logger.warning(f"Unexpected response format for arrivals: {type(data)}")
                return []
            
            logger.info(f"Successfully fetched arrivals for {stop_point_id}")
            return data
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error fetching arrivals: {e.response.status_code} - {e.response.text}")
        raise
    except httpx.RequestError as e:
        logger.error(f"Request error fetching arrivals: {e}")
        raise
