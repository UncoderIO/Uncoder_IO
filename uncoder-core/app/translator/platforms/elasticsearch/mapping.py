from app.translator.platforms.base.lucene.mapping import LuceneMappings


class ElasticSearchMappings(LuceneMappings):
    pass


elasticsearch_mappings = ElasticSearchMappings(platform_dir="elasticsearch")
