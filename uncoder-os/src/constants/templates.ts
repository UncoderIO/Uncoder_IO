export enum TemplatesKeys {
    MinimalRoota = 'Minimal RootA',
    FullRoota = 'Full RootA',
    MinimalSigma = 'Minimal SIGMA',
    FullSigma = 'Full SIGMA',
}

export type TemplateOption = {
  name: TemplatesKeys,
  value: string,
}

export const templates: TemplateOption[] = [
  {
    name: TemplatesKeys.MinimalRoota,
    value: `name: 
details: 
author: 
severity: 
date: 
mitre-attack:
    - 
detection:
    language: 
    body: 
references: 
    - 
license: DRL 1.1`,
  },
  {
    name: TemplatesKeys.FullRoota,
    value: `name: 
details: 
author: 
severity: 
type: 
class: 
date: 
mitre-attack: 
    - 
detection:
    language: 
    body: 
logsource:
    product:                # Sigma or OCSF product
    log_name:               # OCSF log name
    class_name:             # OCSF class
    #category:              # Sigma category
    #service:               # Sigma service
    audit:
        source: 
        enable: 
timeline:
references: 
    - 
tags: 
license: DRL 1.1
version: 
uuid:`,
  },
  {
    name: TemplatesKeys.MinimalSigma,
    value: `title: sigma title
logsource:
    #service:
    category:
    product: windows
detection:
    selection:
        ParentImage|endswith:
            - ''
        Image|endswith:
            - ''
        CommandLine|contains:
            - ''
    condition: selection`,
  },
  {
    name: TemplatesKeys.FullSigma,
    value: `title: sigma title
status:
description:
author:
references:
    -
tags:
    -
logsource:
    #service:
    category:
    product: windows
detection:
    selection:
        ParentImage|endswith:
            - ''
        Image|endswith:
            - ''
        CommandLine|contains:
            - ''
    condition: selection
falsepositives:
    -
level: medium`,
  },
];
