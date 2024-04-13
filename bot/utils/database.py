from database.models.region import Region
from database.connector import session

from bot.utils.enums import RequestType


async def get_regions() -> list[tuple]:
    with session() as s:
        regions = s.query(Region).all()
    response = []
    for region in regions:
        response.append((region.region_id, region.region_name))
    return response


async def get_request_types() -> list[str]:
    resp = []
    for type in RequestType:
        resp.append(type.value)
    return resp
