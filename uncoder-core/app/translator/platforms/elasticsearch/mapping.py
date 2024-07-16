from app.translator.platforms.base.lucene.mapping import LuceneMappings
from app.translator.platforms.elasticsearch.const import (
    elastalert_details,
    elasticsearch_lucene_query_details,
    elasticsearch_rule_details,
    kibana_rule_details,
    xpack_watcher_details,
)

elasticsearch_lucene_query_mappings = LuceneMappings(
    platform_dir="elasticsearch", platform_details=elasticsearch_lucene_query_details
)
elasticsearch_rule_mappings = LuceneMappings(platform_dir="elasticsearch", platform_details=elasticsearch_rule_details)
elastalert_mappings = LuceneMappings(platform_dir="elasticsearch", platform_details=elastalert_details)
kibana_rule_mappings = LuceneMappings(platform_dir="elasticsearch", platform_details=kibana_rule_details)
xpack_watcher_mappings = LuceneMappings(platform_dir="elasticsearch", platform_details=xpack_watcher_details)
