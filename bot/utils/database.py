from database.models.region import Region
from database.connector import session


async def get_regions() -> list[tuple]:
    with session() as s:
        regions = s.query(Region).all()
    response = []
    for region in regions:
        response.append((region.region_id, region.region_name))
    return response
