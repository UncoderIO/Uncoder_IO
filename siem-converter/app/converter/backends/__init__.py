from app.converter.backends.athena.parsers.athena import AthenaParser
from app.converter.backends.athena.renders.athena import AthenaQueryRender
from app.converter.backends.athena.renders.athena_cti import AthenaCTI
from app.converter.backends.carbonblack.renders.carbonblack_cti import CarbonBlackCTI
from app.converter.backends.chronicle.parsers.chronicle import ChronicleParser
from app.converter.backends.chronicle.parsers.chronicle_rule import ChronicleRuleParser
from app.converter.backends.chronicle.renders.chronicle import ChronicleQueryRender
from app.converter.backends.chronicle.renders.chronicle_cti import ChronicleQueryCTI
from app.converter.backends.chronicle.renders.chronicle_rule import ChronicleSecurityRuleRender
from app.converter.backends.crowdstrike.parsers.crowdstrike import CrowdStrikeParser
from app.converter.backends.crowdstrike.renders.crowdstrike import CrowdStrikeQueryRender
from app.converter.backends.crowdstrike.renders.crowdstrike_cti import CrowdStrikeCTI
from app.converter.backends.elasticsearch.parsers.detection_rule import ElasticSearchRuleParser
from app.converter.backends.elasticsearch.parsers.elasticsearch import ElasticSearchParser
from app.converter.backends.elasticsearch.renders.detection_rule import ElasticSearchRuleRender
from app.converter.backends.elasticsearch.renders.elast_alert import ElastAlertRuleRender
from app.converter.backends.elasticsearch.renders.elasticsearch import ElasticSearchQueryRender
from app.converter.backends.elasticsearch.renders.elasticsearch_cti import ElasticsearchCTI
from app.converter.backends.elasticsearch.renders.kibana import KibanaRuleRender
from app.converter.backends.elasticsearch.renders.xpack_watcher import XPackWatcherRuleRender
from app.converter.backends.fireeye_helix.renders.fireeye_helix_cti import FireeyeHelixCTI
from app.converter.backends.graylog.renders.graylog_cti import GraylogCTI
from app.converter.backends.logpoint.renders.logpoint_cti import LogpointCTI
from app.converter.backends.logscale.parsers.logscale import LogScaleParser
from app.converter.backends.logscale.parsers.logscale_alert import LogScaleAlertParser
from app.converter.backends.logscale.renders.logscale_cti import LogScaleCTI
from app.converter.backends.logscale.renders.logscale import LogScaleQueryRender
from app.converter.backends.logscale.renders.logscale_alert import LogScaleAlertRender
from app.converter.backends.microsoft.parsers.microsoft_defender import MicrosoftDefenderQueryParser
from app.converter.backends.microsoft.parsers.microsoft_sentinel import MicrosoftParser
from app.converter.backends.microsoft.parsers.microsoft_sentinel_rule import MicrosoftRuleParser
from app.converter.backends.microsoft.renders.microsoft_defender import MicrosoftDefenderQueryRender
from app.converter.backends.microsoft.renders.microsoft_defender_cti import MicrosoftDefenderCTI
from app.converter.backends.microsoft.renders.microsoft_sentinel import MicrosoftSentinelQueryRender
from app.converter.backends.microsoft.renders.microsoft_sentinel_cti import MicrosoftSentinelCTI
from app.converter.backends.microsoft.renders.microsoft_sentinel_rule import MicrosoftSentinelRuleRender
from app.converter.backends.opensearch.parsers.opensearch import OpenSearchParser
from app.converter.backends.opensearch.renders.opensearch import OpenSearchQueryRender
from app.converter.backends.opensearch.renders.opensearch_cti import OpenSearchCTI
from app.converter.backends.opensearch.renders.opensearch_rule import OpenSearchRuleRender
from app.converter.backends.qradar.parsers.qradar import QradarParser
from app.converter.backends.qradar.renders.qradar import QradarQueryRender
from app.converter.backends.qradar.renders.qradar_cti import QRadarCTI
from app.converter.backends.qualys.renders.qualys_cti import QualysCTI
from app.converter.backends.rsa_netwitness.renders.rsa_netwitness_cti import RSANetwitnessCTI
from app.converter.backends.securonix.renders.securonix_cti import SecuronixCTI
from app.converter.backends.sentinel_one.renders.s1_cti import S1EventsCTI
from app.converter.backends.sigma.parsers.sigma import SigmaParser
from app.converter.backends.sigma.renders.sigma import SigmaRender
from app.converter.backends.snowflake.renders.snowflake_cti import SnowflakeCTI
from app.converter.backends.splunk.parsers.splunk import SplunkParser
from app.converter.backends.splunk.parsers.splunk_alert import SplunkAlertParser
from app.converter.backends.splunk.renders.splunk import SplunkQueryRender
from app.converter.backends.splunk.renders.splunk_alert import SplunkAlertRender
from app.converter.backends.splunk.renders.splunk_cti import SplunkCTI
from app.converter.backends.sumo_logic.renders.sumologic_cti import SumologicCTI

__ALL_RENDERS = (
    SigmaRender(),
    MicrosoftSentinelQueryRender(),
    MicrosoftSentinelRuleRender(),
    MicrosoftDefenderQueryRender(),
    QradarQueryRender(),
    CrowdStrikeQueryRender(),
    SplunkQueryRender(),
    SplunkAlertRender(),
    ChronicleQueryRender(),
    ChronicleSecurityRuleRender(),
    AthenaQueryRender(),
    ElasticSearchQueryRender(),
    LogScaleQueryRender(),
    LogScaleAlertRender(),
    ElasticSearchRuleRender(),
    ElastAlertRuleRender(),
    KibanaRuleRender(),
    XPackWatcherRuleRender(),
    OpenSearchQueryRender(),
    OpenSearchRuleRender()
)

__ALL_PARSERS = (
    AthenaParser(),
    ChronicleParser(),
    ChronicleRuleParser(),
    SplunkParser(),
    SplunkAlertParser(),
    SigmaParser(),
    QradarParser(),
    MicrosoftParser(),
    MicrosoftRuleParser(),
    MicrosoftDefenderQueryParser(),
    CrowdStrikeParser(),
    LogScaleParser(),
    LogScaleAlertParser(),
    ElasticSearchParser(),
    ElasticSearchRuleParser(),
    OpenSearchParser()
)


__ALL_RENDERS_CTI = (
        MicrosoftSentinelCTI(),
        MicrosoftDefenderCTI(),
        QRadarCTI(),
        SplunkCTI(),
        ChronicleQueryCTI(),
        CrowdStrikeCTI(),
        SumologicCTI(),
        ElasticsearchCTI(),
        LogScaleCTI(),
        OpenSearchCTI(),
        FireeyeHelixCTI(),
        CarbonBlackCTI(),
        GraylogCTI(),
        LogpointCTI(),
        QualysCTI(),
        RSANetwitnessCTI(),
        S1EventsCTI(),
        SecuronixCTI(),
        SnowflakeCTI(),
        AthenaCTI()
)
