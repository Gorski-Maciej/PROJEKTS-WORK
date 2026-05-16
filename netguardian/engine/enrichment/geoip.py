import os
from functools import lru_cache

import geoip2.database


@lru_cache(maxsize=1)
def _reader():
    db_path = os.getenv('GEOIP_DB', '/app/data/GeoLite2-City.mmdb')
    if not os.path.exists(db_path):
        return None
    return geoip2.database.Reader(db_path)


def get_geo(ip: str):
    reader = _reader()
    if reader is None:
        return None
    try:
        response = reader.city(ip)
        return {
            'country': response.country.name,
            'city': response.city.name,
            'latitude': response.location.latitude,
            'longitude': response.location.longitude,
        }
    except Exception:
        return None
