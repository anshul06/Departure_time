import httpx
from fastapi import APIRouter, HTTPException
from app.services.tfl_client import get_nearby_stop_points, get_arrivals
from app.logger import logger

router = APIRouter()


@router.get("/departures")
async def get_departures(lat: float, lon: float):
    logger.info(f"Received /departures request lat={lat}, lon={lon}")

    try:
        stops = await get_nearby_stop_points(lat, lon)
        
        if not stops:
            logger.warning(f"No stops found for lat={lat}, lon={lon}")
            return {
                "location": {"lat": lat, "lon": lon},
                "stations": [],
            }
        
        stations = []

        for stop in stops[:3]:
            try:
                stop_id = stop.get("naptanId")
                if not stop_id:
                    logger.warning(f"Stop missing naptanId: {stop}")
                    continue
                
                arrivals = await get_arrivals(stop_id)

                departures = [
                    {
                        "line": a.get("lineName", "Unknown"),
                        "destination": a.get("destinationName", "Unknown"),
                        "in_minutes": max(0, a.get("timeToStation", 0) // 60),
                    }
                    for a in arrivals
                    if isinstance(a, dict)
                ]

                departures = sorted(departures, key=lambda x: x["in_minutes"])[:5]

                stations.append(
                    {
                        "station": stop.get("commonName", "Unknown Station"),
                        "mode": stop.get("modes", ["Unknown"])[0] if stop.get("modes") else "Unknown",
                        "departures": departures,
                    }
                )
            except Exception as e:
                logger.error(f"Error processing stop {stop.get('naptanId', 'unknown')}: {e}")
                continue

        logger.info("Successfully processed departures request")

        return {
            "location": {"lat": lat, "lon": lon},
            "stations": stations,
        }

    except httpx.HTTPStatusError as e:
        error_detail = f"TFL API error: {e.response.status_code}"
        if e.response.status_code == 429:
            error_detail = "Invalid API key or rate limit exceeded. Please check your TFL_API_KEY."
        logger.error(f"HTTP error: {error_detail}")
        raise HTTPException(status_code=e.response.status_code, detail=error_detail)
    except httpx.RequestError as e:
        logger.error(f"Request error: {e}")
        raise HTTPException(status_code=503, detail="Unable to connect to TFL API")
    except Exception as e:
        logger.error(f"Error processing departures request: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
