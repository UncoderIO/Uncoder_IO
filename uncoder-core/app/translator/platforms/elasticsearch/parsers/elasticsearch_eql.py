import re

from app.translator.core.models.platform_details import PlatformDetails
from app.translator.core.models.query_container import RawQueryContainer, TokenizedQueryContainer
from app.translator.core.parser import PlatformQueryParser
from app.translator.managers import parser_manager
from app.translator.platforms.base.lucene.mapping import LuceneMappings
from app.translator.platforms.elasticsearch.const import elastic_eql_query_details
from app.translator.platforms.elasticsearch.mapping import elastic_eql_query_mappings
from app.translator.platforms.elasticsearch.tokenizer import ElasticSearchEQLTokenizer


@parser_manager.register_supported_by_roota
class ElasticSearchEQLQueryParser(PlatformQueryParser):
    details: PlatformDetails = elastic_eql_query_details
    tokenizer = ElasticSearchEQLTokenizer()
    mappings: LuceneMappings = elastic_eql_query_mappings
    query_delimiter_pattern = r"\swhere\s"

    def _parse_query(self, query: str) -> tuple[str, dict[str, list[str]]]:
        log_source = {"category": []}
        if re.search(self.query_delimiter_pattern, query, flags=re.IGNORECASE):
            sp_query = re.split(self.query_delimiter_pattern, query, flags=re.IGNORECASE)
            if sp_query[0].lower() != "all":
                log_source["category"].append(sp_query[0])
            return sp_query[1], log_source
        return query, log_source

    def parse(self, raw_query_container: RawQueryContainer) -> TokenizedQueryContainer:
        query, log_sources = self._parse_query(raw_query_container.query)
        query_tokens = self.get_query_tokens(query)
        query_field_tokens, _, _ = self.get_field_tokens(query_tokens)
        source_mappings = self.get_source_mappings(
            field_tokens=query_field_tokens,
            log_sources=log_sources,
            alt_mapping=raw_query_container.meta_info.source_alt_mapping,
        )
        meta_info = raw_query_container.meta_info
        meta_info.query_fields = query_field_tokens
        meta_info.source_mapping_ids = [source_mapping.source_id for source_mapping in source_mappings]
        return TokenizedQueryContainer(tokens=query_tokens, meta_info=meta_info)
