from dataclasses import dataclass

from app.translator.core.models.platform_details import PlatformDetails

FORTI_SIEM_RULE_DETAILS = {
    "platform_id": "fortisiem-rule",
    "name": "FortiSIEM Rule",
    "platform_name": "Rule",
    "group_id": "forti_siem",
    "group_name": "FortiSIEM",
}


forti_siem_rule_details = PlatformDetails(**FORTI_SIEM_RULE_DETAILS)


FORTI_SIEM_RULE = """
<Rule <header_placeholder>>
  <Name><name_placeholder></Name>
  <IncidentTitle><title_placeholder></IncidentTitle>
  <active>true</active>
  <Description><description_placeholder></Description>
  <DetectionTechnology>Correlation</DetectionTechnology>
  <ignoreSIGMAUpdate>false</ignoreSIGMAUpdate>
  <CustomerScope groupByEachCustomer="true">
    <Include all="true"/>
    <Exclude/>
  </CustomerScope>
  <IncidentDef <incident_def_placeholder>>
    <ArgList><args_list_placeholder></ArgList>
  </IncidentDef>
  <PatternClause window="300">
    <SubPattern displayName="Filter" name="Filter">
      <SingleEvtConstr><query_placeholder></SingleEvtConstr>
      <GroupByAttr><group_by_attr_placeholder></GroupByAttr>
      <GroupEvtConstr>COUNT(*) &gt;= 1</GroupEvtConstr>
    </SubPattern>
  </PatternClause>
  <TriggerEventDisplay>
    <AttrList><attr_list_placeholder></AttrList>
  </TriggerEventDisplay>
</Rule>
"""


@dataclass
class SourceEventTypesContainer:
    default_pattern: str
    event_types_map: dict[int, list[str]]


SOURCES_EVENT_TYPES_CONTAINERS_MAP = {
    "windows_sysmon": SourceEventTypesContainer(
        default_pattern="Win-Sysmon-",
        event_types_map={
            1: ["Win-Sysmon-1-Create-Process"],
            2: ["Win-Sysmon-2-FileCreation-Time-Changed"],
            3: ["Win-Sysmon-3-Network-Connection-IPv4", "Win-Sysmon-3-Network-Connection-IPv6"],
            5: ["Win-Sysmon-5-Process-Terminated"],
            6: ["Win-Sysmon-6-Driver-Loaded"],
            7: ["Win-Sysmon-7-Image-Loaded"],
            8: ["Win-Sysmon-8-CreateRemoteThread"],
            9: ["Win-Sysmon-9-RawAccessRead"],
            10: ["Win-Sysmon-10-ProcessAccess"],
            11: ["Win-Sysmon-11-FileCreate"],
            12: [
                "Win-Sysmon-12-Registry-CreateKey",
                "Win-Sysmon-12-Registry-DeleteKey",
                "Win-Sysmon-12-Registry-CreateValue",
                "Win-Sysmon-12-Registry-DeleteValue",
            ],
            13: ["Win-Sysmon-13-Registry-SetValue"],
            14: ["Win-Sysmon-14-Registry-RenameKey", "Win-Sysmon-14-Registry-RenameValue"],
            15: ["Win-Sysmon-15-FileCreateStreamHash"],
            16: ["Win-Sysmon-16-Config-State-Changed"],
            17: ["Win-Sysmon-17-PipeCreated"],
            18: ["Win-Sysmon-18-PipeConnected"],
            19: ["Win-Sysmon-19-WMIEventFilterActivity"],
            20: ["Win-Sysmon-20-WMIEventConsumerActivity"],
            21: ["Win-Sysmon-21-WMIEventConsumerToFilterActivity"],
            22: ["Win-Sysmon-22-DNSQuery"],
        },
    ),
    "registry_event": SourceEventTypesContainer(
        default_pattern="Win-Sysmon-",
        event_types_map={
            1: ["Win-Sysmon-1-Create-Process"],
            2: ["Win-Sysmon-2-FileCreation-Time-Changed"],
            3: ["Win-Sysmon-3-Network-Connection-IPv4", "Win-Sysmon-3-Network-Connection-IPv6"],
            5: ["Win-Sysmon-5-Process-Terminated"],
            6: ["Win-Sysmon-6-Driver-Loaded"],
            7: ["Win-Sysmon-7-Image-Loaded"],
            8: ["Win-Sysmon-8-CreateRemoteThread"],
            9: ["Win-Sysmon-9-RawAccessRead"],
            10: ["Win-Sysmon-10-ProcessAccess"],
            11: ["Win-Sysmon-11-FileCreate"],
            12: [
                "Win-Sysmon-12-Registry-CreateKey",
                "Win-Sysmon-12-Registry-DeleteKey",
                "Win-Sysmon-12-Registry-CreateValue",
                "Win-Sysmon-12-Registry-DeleteValue",
            ],
            13: ["Win-Sysmon-13-Registry-SetValue"],
            14: ["Win-Sysmon-14-Registry-RenameKey", "Win-Sysmon-14-Registry-RenameValue"],
            15: ["Win-Sysmon-15-FileCreateStreamHash"],
            16: ["Win-Sysmon-16-Config-State-Changed"],
            17: ["Win-Sysmon-17-PipeCreated"],
            18: ["Win-Sysmon-18-PipeConnected"],
            19: ["Win-Sysmon-19-WMIEventFilterActivity"],
            20: ["Win-Sysmon-20-WMIEventConsumerActivity"],
            21: ["Win-Sysmon-21-WMIEventConsumerToFilterActivity"],
            22: ["Win-Sysmon-22-DNSQuery"],
        },
    ),
    "windows_system": SourceEventTypesContainer(
        default_pattern="Win-System-",
        event_types_map={
            104: ["Win-System-Microsoft-Windows-Eventlog-104"],
            7036: ["Win-System-Service-Control-Manager-7036-.*"],
            7045: ["Win-System-Service-Control-Manager-7045"],
        },
    ),
    "windows_powershell": SourceEventTypesContainer(default_pattern="Win-PowerShell-", event_types_map={}),
    "windows_powershell_classic": SourceEventTypesContainer(default_pattern="Win-PowerShell-", event_types_map={}),
    "windows_security": SourceEventTypesContainer(
        default_pattern="Win-Security-",
        event_types_map={
            4768: ["Win-Security-4768-success", "Win-Security-4768-failure"],
            4769: ["Win-Security-4769-failure", "Win-Security-4769-success"],
        },
    ),
    "windows_app": SourceEventTypesContainer(default_pattern="Win-App-", event_types_map={}),
    "windows_application": SourceEventTypesContainer(default_pattern="Win-App-", event_types_map={}),
    "windows_wmi_event": SourceEventTypesContainer(
        default_pattern="Win-Sysmon-",
        event_types_map={
            19: ["Win-Sysmon-19-WMI-Event-Filter-Activity"],
            20: ["Win-Sysmon-20-WMI-Event-Consumer-Activity"],
            21: ["Win-Sysmon-21-WMI-Event-ConsumerToFilter-Activity"],
        },
    ),
    "windows_appxdeployment": SourceEventTypesContainer(
        default_pattern="Win-AppXDeployment-Server-",
        event_types_map={
            400: ["Win-AppXDeployment-Server-400"],
            401: ["Win-AppXDeployment-Server-401"],
            157: ["Win-AppXDeployment-Server-157"],
        },
    ),
    "windows_appxdeployment_server": SourceEventTypesContainer(
        default_pattern="Win-AppXDeployment-Server-",
        event_types_map={
            400: ["Win-AppXDeployment-Server-400"],
            401: ["Win-AppXDeployment-Server-401"],
            157: ["Win-AppXDeployment-Server-157"],
        },
    ),
    "windows_appxpackaging_om": SourceEventTypesContainer(
        default_pattern="Win-AppXDeployment-Server-",
        event_types_map={
            400: ["Win-AppXDeployment-Server-400"],
            401: ["Win-AppXDeployment-Server-401"],
            157: ["Win-AppXDeployment-Server-157"],
        },
    ),
    "windows_firewall_as": SourceEventTypesContainer(
        default_pattern="Win-Firewall-AS-",
        event_types_map={
            2002: ["Win-Firewall-AS-2002"],
            2083: ["Win-Firewall-AS-2083"],
            2003: ["Win-Firewall-AS-2003"],
            2082: ["Win-Firewall-AS-2082"],
            2008: ["Win-Firewall-AS-2008"],
        },
    ),
    "windows_provider_name": SourceEventTypesContainer(
        default_pattern="Win-PrintService-",
        event_types_map={
            216: ["Win-PrintService-Setup-Succeeded"],
            325: ["Win-PrintService-Remove-Printer-Failed"],
            322: ["Win-PrintService-Publish-Printer-Failed"],
            323: ["Win-PrintService-Publish-Printer-Failed"],
            326: ["Win-PrintService-Publish-Printer-Failed"],
            327: ["Win-PrintService-Publish-Printer-Failed"],
            328: ["Win-PrintService-Publish-Printer-Failed"],
            329: ["Win-PrintService-Publish-Printer-Failed"],
            331: ["Win-PrintService-Publish-Printer-Failed"],
            333: ["Win-PrintService-Publish-Printer-Failed"],
        },
    ),
    "windows_security_mitigations": SourceEventTypesContainer(
        default_pattern="Win-Security-Mitigation-",
        event_types_map={11: ["Win-Security-Mitigation-11"], 12: ["Win-Security-Mitigation-12"]},
    ),
    "windows_dns_client": SourceEventTypesContainer(
        default_pattern="Win-DNS-Client-", event_types_map={3008: ["Win-DNS-Client-3008"]}
    ),
    "windows_bits_client": SourceEventTypesContainer(
        default_pattern="Win-App-Microsoft-Windows-Bits-Client-",
        event_types_map={16403: ["Win-App-Microsoft-Windows-Bits-Client-16403"]},
    ),
    "windows_diagnosis_scripted": SourceEventTypesContainer(
        default_pattern="Win-Diagnostics-Scripted-", event_types_map={101: ["Win-Diagnostics-Scripted-101"]}
    ),
    "windows_msexchange_management": SourceEventTypesContainer(
        default_pattern="Win-MSExchange-Management-", event_types_map={6: ["Win-MSExchange-Management-6"]}
    ),
    "windows_file_block": SourceEventTypesContainer(
        default_pattern="Win-Sysmon-", event_types_map={27: ["Win-Sysmon-27-FileBlockExecutable"]}
    ),
    "windows_shell_core": SourceEventTypesContainer(
        default_pattern="Win-Shell-Core-", event_types_map={28115: ["Win-Shell-Core-28115"]}
    ),
    "windows_codeintegrity_operational": SourceEventTypesContainer(
        default_pattern="Win-CodeIntegrity-Operational-",
        event_types_map={
            3023: ["Win-CodeIntegrity-Operational-3023"],
            3033: ["Win-CodeIntegrity-Operational-3033"],
            3077: ["Win-CodeIntegrity-Operational-3077"],
        },
    ),
    "windows_openssh": SourceEventTypesContainer(
        default_pattern="Win-OpenSSH-", event_types_map={4: ["Win-OpenSSH-4"]}
    ),
}
