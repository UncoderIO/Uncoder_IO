from app.translator.tools.custom_enum import CustomEnum


class IPLocationType(CustomEnum):
    asn = "ip_loc_asn"
    asn_org = "ip_loc_asn_org"
    city = "ip_loc_city"
    continent = "ip_loc_continent"
    country = "ip_loc_country"
    lat_lon = "ip_loc_lat_lon"
    region = "ip_loc_region"
    timezone = "ip_loc_timezone"


class TimeType(CustomEnum):
    timestamp = "timestamp"
