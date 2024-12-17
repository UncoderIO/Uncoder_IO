from app.translator.platforms.base.lucene.mapping import LuceneMappings
from app.translator.platforms.elasticsearch.const import (
    elastalert_details,
    elastic_eql_query_details,
    elasticsearch_esql_query_details,
    elastic_eql_query_details,
    elasticsearch_lucene_query_details,
    elasticsearch_rule_details,
    kibana_rule_details,
    xpack_watcher_details,
)

DEFAULT_MAPPING_NAME = "default"

elasticsearch_lucene_query_mappings = LuceneMappings(
    platform_dir="elasticsearch", platform_details=elasticsearch_lucene_query_details
)
elasticsearch_rule_mappings = LuceneMappings(platform_dir="elasticsearch", platform_details=elasticsearch_rule_details)
elastalert_mappings = LuceneMappings(platform_dir="elasticsearch", platform_details=elastalert_details)
kibana_rule_mappings = LuceneMappings(platform_dir="elasticsearch", platform_details=kibana_rule_details)
xpack_watcher_mappings = LuceneMappings(platform_dir="elasticsearch", platform_details=xpack_watcher_details)
elastic_eql_query_mappings = LuceneMappings(platform_dir="elasticsearch", platform_details=elastic_eql_query_details)


class ElasticESQLMappings(LuceneMappings):
    is_strict_mapping: bool = True
    skip_load_default_mappings = True


esql_query_mappings = ElasticESQLMappings(
    platform_dir="elasticsearch_esql", platform_details=elasticsearch_esql_query_details
)
