from app.translator.platforms.base.lucene.mapping import LuceneMappings


class GraylogMappings(LuceneMappings):
    pass


graylog_mappings = GraylogMappings(platform_dir="graylog")
