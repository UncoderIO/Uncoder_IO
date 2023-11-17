from app.converter.platforms.athena.parsers.athena import AthenaParser
from app.converter.platforms.athena.renders.athena import AthenaQueryRender
from app.converter.platforms.athena.renders.athena_cti import AthenaCTI
from app.converter.platforms.carbonblack.renders.carbonblack_cti import CarbonBlackCTI
from app.converter.platforms.chronicle.parsers.chronicle import ChronicleParser
from app.converter.platforms.chronicle.parsers.chronicle_rule import ChronicleRuleParser
from app.converter.platforms.chronicle.renders.chronicle import ChronicleQueryRender
from app.converter.platforms.chronicle.renders.chronicle_cti import ChronicleQueryCTI
from app.converter.platforms.chronicle.renders.chronicle_rule import ChronicleSecurityRuleRender
from app.converter.platforms.crowdstrike.parsers.crowdstrike import CrowdStrikeParser
from app.converter.platforms.crowdstrike.renders.crowdstrike import CrowdStrikeQueryRender
from app.converter.platforms.crowdstrike.renders.crowdstrike_cti import CrowdStrikeCTI
from app.converter.platforms.elasticsearch.parsers.detection_rule import ElasticSearchRuleParser
from app.converter.platforms.elasticsearch.parsers.elasticsearch import ElasticSearchParser
from app.converter.platforms.elasticsearch.renders.detection_rule import ElasticSearchRuleRender
from app.converter.platforms.elasticsearch.renders.elast_alert import ElastAlertRuleRender
from app.converter.platforms.elasticsearch.renders.elasticsearch import ElasticSearchQueryRender
from app.converter.platforms.elasticsearch.renders.elasticsearch_cti import ElasticsearchCTI
from app.converter.platforms.elasticsearch.renders.kibana import KibanaRuleRender
from app.converter.platforms.elasticsearch.renders.xpack_watcher import XPackWatcherRuleRender
from app.converter.platforms.fireeye_helix.renders.fireeye_helix_cti import FireeyeHelixCTI
from app.converter.platforms.graylog.renders.graylog_cti import GraylogCTI
from app.converter.platforms.logpoint.renders.logpoint_cti import LogpointCTI
from app.converter.platforms.logscale.parsers.logscale import LogScaleParser
from app.converter.platforms.logscale.parsers.logscale_alert import LogScaleAlertParser
from app.converter.platforms.logscale.renders.logscale_cti import LogScaleCTI
from app.converter.platforms.logscale.renders.logscale import LogScaleQueryRender
from app.converter.platforms.logscale.renders.logscale_alert import LogScaleAlertRender
from app.converter.platforms.microsoft.parsers.microsoft_defender import MicrosoftDefenderQueryParser
from app.converter.platforms.microsoft.parsers.microsoft_sentinel import MicrosoftParser
from app.converter.platforms.microsoft.parsers.microsoft_sentinel_rule import MicrosoftRuleParser
from app.converter.platforms.microsoft.renders.microsoft_defender import MicrosoftDefenderQueryRender
from app.converter.platforms.microsoft.renders.microsoft_defender_cti import MicrosoftDefenderCTI
from app.converter.platforms.microsoft.renders.microsoft_sentinel import MicrosoftSentinelQueryRender
from app.converter.platforms.microsoft.renders.microsoft_sentinel_cti import MicrosoftSentinelCTI
from app.converter.platforms.microsoft.renders.microsoft_sentinel_rule import MicrosoftSentinelRuleRender
from app.converter.platforms.opensearch.parsers.opensearch import OpenSearchParser
from app.converter.platforms.opensearch.renders.opensearch import OpenSearchQueryRender
from app.converter.platforms.opensearch.renders.opensearch_cti import OpenSearchCTI
from app.converter.platforms.opensearch.renders.opensearch_rule import OpenSearchRuleRender
from app.converter.platforms.qradar.parsers.qradar import QradarParser
from app.converter.platforms.qradar.renders.qradar import QradarQueryRender
from app.converter.platforms.qradar.renders.qradar_cti import QRadarCTI
from app.converter.platforms.qualys.renders.qualys_cti import QualysCTI
from app.converter.platforms.rsa_netwitness.renders.rsa_netwitness_cti import RSANetwitnessCTI
from app.converter.platforms.securonix.renders.securonix_cti import SecuronixCTI
from app.converter.platforms.sentinel_one.renders.s1_cti import S1EventsCTI
from app.converter.platforms.sigma.parsers.sigma import SigmaParser
from app.converter.platforms.sigma.renders.sigma import SigmaRender
from app.converter.platforms.snowflake.renders.snowflake_cti import SnowflakeCTI
from app.converter.platforms.splunk.parsers.splunk import SplunkParser
from app.converter.platforms.splunk.parsers.splunk_alert import SplunkAlertParser
from app.converter.platforms.splunk.renders.splunk import SplunkQueryRender
from app.converter.platforms.splunk.renders.splunk_alert import SplunkAlertRender
from app.converter.platforms.splunk.renders.splunk_cti import SplunkCTI
from app.converter.platforms.sumo_logic.renders.sumologic_cti import SumologicCTI

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
