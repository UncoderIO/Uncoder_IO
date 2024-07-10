from app.translator.platforms.base.lucene.mapping import LuceneMappings
from app.translator.platforms.opensearch.const import opensearch_query_details, opensearch_rule_details

opensearch_query_mappings = LuceneMappings(platform_dir="opensearch", platform_details=opensearch_query_details)
opensearch_rule_mappings = LuceneMappings(platform_dir="opensearch", platform_details=opensearch_rule_details)
