<p align="left">
  <img src="images/uncoder_io_logo_double.png" width="120" height="120">
</p>

# What is Uncoder IO
Uncoder IO is an open source version of it's SaaS counterpart https://uncoder.io and it's AI co-pilot version Uncoder AI. 
Since 2018, Uncoder.IO is a fast, private and easy to use online translator for Sigma Rules, maintaining 100% privacy of its users. 
An open source Uncoder IO expands use cases into following:
- Translation from Sigma Rules, a generic rule format for SIEM systems, to specific SIEM, EDR and Data Lake languages
- IOC packaging from any non-binary format such as PDF, text, STIX, OpenIOC to speicifc SIEM, EDR and Data Lake languages
- Translation from RootA Rules, the newly released language for collective cyber defense, to specific SIEM, EDR and Data Lake languages.

Uncoder is developed by the team of Detection Engineers, Threat Hunters and CTI Analysts from Ukraine, Europe, USA, Argentina and Australia to perform their daily job and nightly cyber defense hobbies faster, better and making their outcomes easier to share for collective good. 


![Uncoder IO Overview](images/uncoder_io_overview.png)

**Table of Contents:**
- [Why Uncoder IO](#heart_eyes_cat-why-uncoder-io)
- [Supported Language Formats](#dna-supported-language-formats)
- [Installation](#computer-installation)
- [Online Version](#evergreen_tree-online-version)
- [How to Use](#mortar_board-how-to-use)
- [How to Contribute](#bulb-how-to-contribute)
- [Questions & Feedback](#mailbox_with_no_mail-questions--feedback)
- [Maintainers](#wrench-maintainers)
- [Credits](#kissing_heart-credits)
- [Licenses](#briefcase-licenses)
- [Resources & Useful Links](#book-resources--useful-links)

# :heart_eyes_cat: Why Uncoder IO

## :pretzel: RootA & Sigma Translation Engine

Uncoder IO supports automated translation of RootA and Sigma rules into multiple SIEM, EDR, XDR, and Data Lake formats. 
- **Sigma** is a generic and open signature format that allows you to describe relevant log events in a straightforward manner, which received industry adoption across 155 countries by over 8000 organizations according to SOC Prime's download and translation statistics. 
 
- **RootA** is an open source language which supports query definition directly in specific SIEM languages, vendor-agnostic correlation syntax, MITRE ATT&CK 14.0 for code autocompletion, log source taxonomy autocomplete function based on Amazon's OCSF or Sigma. RootA+Uncoder serve as the first bridge towards full cyber security languages compatibility, where one day, knowing one speicific language (say SPL or KQL) or generic language (say RootA or Sigma) would mean that you have master expertise in them all. This way, your complex detection logic can be rendered in other languages in an automated fashion. In case a native rule or query contains functions unsupported by RootA or target technology, those functions won’t be translated, with a corresponding note appended to the code translation. This is done so that experts can either manually complete translations if they know both source and destination languages, or use Uncoder AI to manually take care of such scenarios. If sharing with Sigma was easy, sharing with RootA is natural and future proof.

## :pizza: RootA & Sigma Rule Editor

Uncoder IO supports a built-in Sigma and RootA rules autocompletion wizard suggesting code enhancements with latest MITRE ATT&CK and log source dictionaries to streamline the rule creation process. AI or not, Uncoder is here to make it easier to code.

## :popcorn: IOC Query Generator

Uncoder IO acts as an open-source IOC packager helping CTI and SOC analysts as well as Threat Hunters to quickly parse any number of IOCs directly from from any digital non-binary format(a simple copy-paste of a web page, CSV, OpenIOC, PDF, STIX etc.) and convert them into performance-optimized IOC queries ready to run in a chosen security analytics platform. As Indicators of Compromise sharing are regulated by TLP, it is not advised to share them in Sigma or RootA rules, as the latter are not part of threat intelligence and thus are shared easily without borders. Yet, we need IOC matching just as we need Threat Behavior detections, so Uncoder IO is made to help solve these both tasks in an easy to use and intuitive manner.

## :smile_cat: Full Privacy

Uncoder IO can be ran on prem without a need for internet connection, thus supporting air gapped networks operation. We do however suggest to check for updates and deploy them regurarly. Meanwhile a SaaS version still ensures 100% privacy with no cookie tracking, no data or code logging, or sharing with third parties. Even with options Uncoder AI functions, you are always in control of your code and data.

# :dna: Supported Language Formats
RootA and Sigma Rules can be translated into the following formats:
- AWS OpenSearch Query - `opensearch-lucene-query`
- AWS Athena Query (Security Lake) - `athena-sql-query`
- Falcon LogScale Query - `logscale-lql-query`
- Falcon LogScale Rule - `logscale-lql-rule`
- Splunk Query - `splunk-spl-query`
- Splunk Alert - `splunk-spl-rule`
- Microsoft Sentinel Query - `sentinel-kql-query`
- Microsoft Sentinel Rule - `sentinel-kql-rule`
- Microsoft Defender for Endpoint Query - `mde-kql-query`
- IBM QRadar Query - `qradar-aql-query`
- CrowdStrike Query - `crowdstrike-spl-query`
- Elasticsearch Query - `elastic-lucene-query`
- Elasticsearch Rule - `elastic-lucene-rule`
- Sigma Rule - `sigma-yml-rule`
- Chronicle Security Query - `chronicle-yaral-query`
- Chronicle Security Rule - `chronicle-yaral-rule`


IOC-based queries can be generated in the following formats:
- Microsoft Sentinel Query - `sentinel-kql-query`
- Microsoft Defender for Endpoint Query - `mde-kql-query`
- Splunk Query - `splunk-spl-query`
- CrowdStrike Query - `crowdstrike-spl-query`
- Elasticsearch Query - `elastic-lucene-query`
- AWS OpenSearch Query - `opensearch-lucene-query`
- Falcon LogScale Query - `logscale-lql-query`
- IBM QRadar Query - `qradar-aql-query`
- AWS Athena Query (Security Lake) - `athena-sql-query`
- Chronicle Security Query - `chronicle-yaral-query`

The following types of IOCs are supported:  
- Hash  
- Domain  
- URL  
- IP  
- Email  
- File  

TODO list of languages we will support shortly:
- Graylog
- Devo
- LimaCharlie
- Sumo Logic
- Sumo Logic CSE
- ArcSight
- Databricks
- Cribl
- FortiSIEM
- Exabeam
- Palo Alto Cortex XSOAR
- ElastAlert 
- FireEye OpenIOC
- SentinelOne
- Datadog
- FireEye Helix
- Logpoint
- RSA NetWitness
- PowerShell
- Snowflake
- SQL
- VMware Carbon Black
- Apache Kafka ksqlDB
- HawkSearch
- Regex Grep
- Logiq
- Qualys
- Securonix
- STIX
- StreamAlert
- Sysmon
- UberAgent ESA

# :computer: Installation
Uncoder IO can be installed in a following manner:
  1. Docker container with web server and UI (available)
  2. Docker continer API and CLI only (work in progress)
  3. Build from source code directly
  4. Ready to use as SaaS, privately with no registration or cookies at https://uncoder.io
  5. Ready to use at SOC Prime SaaS with private AI augmentation, SOC 2 Type II certified environment and supporting ToS on data privacy, GDPR etc.

## Requirements
* Host with Windows, Linux, or other operating system supported by Docker
* These packages should be installed on the host:
    * Docker v23.0.1 or newer
    * Docker Compose v2.21.0 or newer
    * Python 3.9 or newer

## Launch Instructions
1. Download the `UncoderIO-main` archive and unpack it.
2. In the CLI, go to the folder where the unpacked files are:
```
cd UncoderIO-main/
```
3. Run the following command to launch a Docker container:
```
docker-compose up -d
```
4. Open `http://localhost:4010/` in your browser and you are ready to go.

# :evergreen_tree: Online Version
You can use the online open-source version of Uncoder IO at [https://uncoder.io/](https://uncoder.io/). It's free, doesn't require registration, and doesn't collect or store any user data whatsoever.

# :mortar_board: How to Use

## :rocket: Translation
1. Select input type:
    - RootA rule
    - Sigma rule
2. Paste or upload a rule in the selected language into the input panel.
3. Select the output (language, content type, and data schema)
4. Click Translate.

If the input rule cannot be translated, you'll see an error message. When translating a RootA rule, any functions that are not supported in the target language or are not yet supported by Uncoder IO will be listed in the output as a comment.

## :flashlight: IOC-based Query Generation
1. Select IoCs as the input type.
2. Paste or upload text with Indicators of Compromise in the left panel.
3. Make parsing configurations:
    - **Select all:** all listed options are applied
    - **Replace (.) [.] {.} with dot**
    - **Replace hxxp with http**: this functionality is case insensitive, so hXXp, HXXP, HXXp, and hXXP are replaced as well
    - **Exclude Private & Reserved Networks:** private and reserved IP addresses like 224.0.0.0/4 or 127.0.0.0/8 are ignored during IOC recognition
4. Select the output language.
5. Make generation settings:
    - Select what IOC types to use for queries:
        - Hash
        - Domain
        - URL
        - IP
        - Email
        - File
    - Set the number of IOCs per query to take into account the performance of your platform
    - Select what hash types to use for queries if the hash is enabled as an IOC type
    - Define exceptions: specify hashes, domains, IPs, emails, files, or URLs (in full or only partially) you want to exclude from your queries
6. Click Translate.

## :coffee: Writing rules
Write a RootA or Sigma rule in the input panel. Benefit from code templates, syntax highlighting, autocomplete suggester with MITRE ATT&CK, and other nice little features that improve coding experience.

# :bulb: How to Contribute
Thank you for your interest in the Uncoder IO open-source project! Your contribution really matters in evolving the project and helping us make Uncoder IO even more useful for the global cyber defender community.

To submit your pull request with your ideas or suggestions for changes, take the following steps:

1. Fork the [Uncoder repository](https://github.com/UncoderIO/UncoderIO) and clone your fork to your local environment.
2. Create a new feature branch, in which you’re going to make your changes.
3. Сommit your changes to your newly created feature branch.
4. Push the changes to your fork.
5. Create a new Pull Request  
    a. Clicking the New Pull Request button.  
    b. Select your fork along with a feature branch.  
    c. Provide a title and a description of your changes. Make sure they are both clear and informative.  
    d. Finally, submit your Pull Request and wait for its approval.  

Thank you for your contribution to the Uncoder IO project!

# :mailbox_with_no_mail: Questions & Feedback
Please submit your technical feedback and suggestions to support@socprime.com or the dedicated **Uncoder** channel in [SOC Prime’s Discord](https://discord.gg/socprime). Also, refer to the [guidance for contributors](#how-to-contribute) to support the Uncoder IO project or simply [report issues](https://github.com/UncoderIO/UncoderIO/issues).

# :wrench: Maintainers
Since 2018, the SOC Prime team has been developing Uncoder from the ground up. The first steps were our support of Sigma rules and the Uncoder IO project, an online yet fully private IDE for detection engineering. Now, the SOC Prime Team shares Uncoder IO as an open-source project.

Uncoder IO project is maintained by SOC Prime, and while any suggestions and reported issues are welcome, the ultimate decision to accept a pull request or not, will be up to SOC Prime's R&D team. 

# :kissing_heart: Credits
We are genuinely grateful to security professionals who contribute their time, expertise, and creativity to evolve the Uncoder open-source project.

# :briefcase: Licenses
Uncoder IO Comunity Edition is licensed under Apache 2.0. Commercial Edition features that are released as open-source can be used non-commercially if you do not have a paid SOC Prime subscription. Commercial use rights are complimentary with SOC Prime SaaS license. Please see [LICENSE](https://github.com/UncoderIO/UncoderIO/blob/main/LICENSE/) for details on the Uncoder IO licensing.

# :book: Resources & Useful Links
[Uncoder IO](https://uncoder.io/) - free online translation engine for RootA, Sigma, and IOC-based queries  
[Uncoder AI](https://tdm.socprime.com/uncoder-ai) - SaaS version of Uncoder acting as advanced IDE for detection engineering  
[RootA.IO](https://roota.io/) - the main website page of the single language for threat detection & response  
[SOC Prime Platform](https://tdm.socprime.com/login) - the industry-first platform for collective cyber defense  
[About SOC Prime](https://socprime.com/) - learn more about SOC Prime and its mission
