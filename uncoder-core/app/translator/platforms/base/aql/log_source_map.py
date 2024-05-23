from dataclasses import dataclass


@dataclass
class AQLLogSourceMap:
    name: str
    id_map: dict[str, int]


CATEGORYNAME_ID_MAP = {
    "ACL Permit": 4012,
    "Successful Registry Modification": 8012,
    "File Created": 8028,
    "Process Creation Success": 8110,
    "DNS In Progress": 18081,
    "Object Load Success": 19247,
}

DEVICETYPE_ID_MAP = {
    "Configurable Firewall Filter": 4,
    "Juniper Networks Firewall and VPN": 5,
    "Cisco PIX Firewall": 6,
    "Apache HTTP Server": 10,
    "Linux OS": 11,
    "Microsoft Windows Security Event Log": 12,
    "Microsoft IIS": 13,
    "Cisco Adaptive Security Appliance (ASA)": 41,
    "Squid Web Proxy": 46,
    "F5 Networks BIG-IP LTM": 49,
    "Fortinet FortiGate Security Gateway": 73,
    "Symantec Gateway Security (SGS) Appliance": 82,
    "Mac OS X": 102,
    "Blue Coat SG Appliance": 103,
    "Nortel Switched Firewall 6000": 104,
    "Nortel Switched Firewall 5100": 120,
    "Imperva SecureSphere": 154,
    "ISC BIND": 185,
    "Microsoft ISA": 191,
    "Cisco ACE Firewall": 194,
    "Risk Manager Default Question": 200,
    "Palo Alto PA Series": 206,
    "Oracle BEA WebLogic": 239,
    "Barracuda Spam & Virus Firewall": 278,
    "F5 Networks BIG-IP AFM": 296,
    "Zscaler Nss": 331,
    "Vormetric Data Security": 340,
    "Amazon AWS CloudTrail": 347,
    "Microsoft DNS Debug": 384,
    "Microsoft Office 365": 397,
    "Microsoft Azure Platform": 413,
    "NGINX HTTP Server": 439,
    "Microsoft Azure Active Directory": 445,
    "Google Cloud Platform Firewall": 455,
    "Amazon AWS Network Firewall": 456,
}

QID_NAME_ID_MAP = {
    "ProcessAccess": 5001829,
    "FileCreateStreamHash": 5001834,
    "Driver loaded": 5001843,
    "CreateRemoteThread": 5001845,
}

LOG_SOURCE_FUNCTIONS_MAP = {
    r"CATEGORYNAME\(category\)": AQLLogSourceMap(name="category", id_map=CATEGORYNAME_ID_MAP),
    r"LOGSOURCETYPENAME\(devicetype\)": AQLLogSourceMap(name="devicetype", id_map=DEVICETYPE_ID_MAP),
    r"QIDNAME\(qid\)": AQLLogSourceMap(name="qid", id_map=QID_NAME_ID_MAP),
}
