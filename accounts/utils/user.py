import random
import functools
import geoip2.database
from django.conf import settings
from logger_egine import logger

LOG_INDEX = "Account Utils"

TEST_IPS = [
    {
        "ip": "128.101.101.101",
        "country": "United States",
        "region": "Minnesota",
        "city": "Minneapolis",
        "latitude": 44.9733,
        "longitude": -93.2323
    },
    {
        "ip": "8.8.8.8",
        "country": "United States",
        "region": "California",
        "city": "Mountain View",
        "latitude": 37.4056,
        "longitude": -122.0775
    },
    {
        "ip": "66.102.0.0",
        "country": "United States",
        "region": "California",
        "city": "Mountain View",
        "latitude": 37.4056,
        "longitude": -122.0775
    },
    {
        "ip": "185.199.108.153",
        "country": "United States",
        "region": "California",
        "city": "San Francisco",
        "latitude": 37.7749,
        "longitude": -122.4194
    },
    {
        "ip": "51.255.147.85",
        "country": "France",
        "region": "Île-de-France",
        "city": "Paris",
        "latitude": 48.8566,
        "longitude": 2.3522
    },
    {
        "ip": "192.168.1.1",
        "country": "Private Network",
        "region": "N/A",
        "city": "N/A",
        "latitude": "N/A",
        "longitude": "N/A"
    },
    {
        "ip": "203.0.113.0",
        "country": "N/A",
        "region": "N/A",
        "city": "N/A",
        "latitude": "N/A",
        "longitude": "N/A"
    }
]


def get_client_ip(request):
    """This method will return the IP address of the client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    if ip == '127.0.0.1':
        return random.choice([ip.get("ip") for ip in TEST_IPS])
    return ip


@functools.lru_cache(32)
def get_client_loc_details(ip_address):
    try:
        print(f"Received IP: {ip_address}")

        # This reader object should be reused across lookups as creation of it is
        # expensive.
        # with geoip2.database.Reader('/path/to/maxmind-database.mmdb') as reader:
        with geoip2.database.Reader(settings.GEOIP_DB_PATH) as reader:
            response = reader.city(ip_address)
            return {
                "ip_address": ip_address,
                "country_iso_code": response.country.iso_code,
                "country_name": response.country.name,
                "city_name": response.city.name,
                "postal_code": response.postal.code,
                "latitude": response.location.latitude,
                "longitude": response.location.longitude,
                "network": str(response.traits.network if response.traits.network else ""),
                "subdivision_name": response.subdivisions.most_specific.name,
                "subdivision_iso_code": response.subdivisions.most_specific.iso_code
            }
    except Exception as geo_err:
        logger.error(LOG_INDEX, f"Exception occurred while fetching geoip data, Exception: {geo_err}")
    return {}
