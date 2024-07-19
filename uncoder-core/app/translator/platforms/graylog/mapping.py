from app.translator.platforms.base.lucene.mapping import LuceneMappings
from app.translator.platforms.graylog.const import graylog_query_details

graylog_query_mappings = LuceneMappings(platform_dir="graylog", platform_details=graylog_query_details)
