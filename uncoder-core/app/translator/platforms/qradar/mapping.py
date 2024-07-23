from app.translator.platforms.base.aql.mapping import AQLMappings
from app.translator.platforms.qradar.const import qradar_query_details

qradar_query_mappings = AQLMappings(platform_dir="qradar", platform_details=qradar_query_details)
