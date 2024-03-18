# Instructions on Adding New Renders
## General
The translation engine of Uncoder IO is conceptually composed of renders, parsers, and mapping files for each supported language.
- A render is a component that generates the target query/rule from a source language (Sigma, Roota).
- A parser is a component that parses the source rule into objects that consequently are used to generate the destination query/rule by the render.
- A mapping file is a dictionary that maps the source fields to target fields as well as source log sources to target log sources.

Uncoder IO supports the following parsers:
- Roota
- Sigma
- IOCs

We encourage you to contribute renders that enable translating from Roota, Sigma, and IOCs into your SIEM, EDR/XDR, or Data Lake.

You can find the list of supported target platforms in the [platforms](https://github.com/UncoderIO/Uncoder_IO/tree/main/translator/app/translator/platforms) directory.

## How to Add a New Render

All code related to translation has to be in the directory with the corresponding platform name in `uncoder-core/app/translator/platforms`.

- `uncoder-core/app/translator/platforms/<platform_name>/renders` – a directory that contains platform renders for different content types (such as rules and queries translated from a source language or queries generated based on parsed IOCs).
- `const.py` – a Python file that contains metainformation about the platform.
- `escape_manager.py` – a Python file that contains classes describing the rules of escaping special characters.
- `mapping.py` – a Python file that contains classes that describe working with mappings.

To add a new render:

1. Create a directory with the platform name in `app/translator/platforms/`.
2. Describe the metainformation about the platform in the `const.py` file.
3. Create a class that processes mappings in the `mapping.py` file.
4. Create a class that processes special characters in the `escaping_manager.py` file.
5. Create the `renders` directory in `uncoder-core/app/translator/platforms/<platform_name>/`.
6. Create a file with the name that matches the name of the platform.
7. The render is composed of two classes:  
    a. `BaseQueryRender` – the class that describes the general mechanism of rendering a query from the tokens parsed from the input query.  
    b. `BaseQueryFieldValue` – the class that describes the mechanism of creating the `Field-Value` component of the query.  


## Render Classes
These classes should be described in the `uncoder-core/app/translator/platforms/<platform_name>/renders/<platform_name>.py` file.

### BaseQueryRender Class

The class has the following attributes:
- `mappings` – a class responsinble for working with mapping of fields and tables/indexes
- `details` – the metainformation about the platform (described in the `const.py` file)
- `is_strict_mapping` – a boolean flag that defines if the render's mapping is strict. When set to `True`, the render returns an error if a field has no mapping
- `platform_functions` – a class responsible for parsing and rendering functions
- `or_token/and_token/not_token` – corresponding platform operators that should be used when generating the target query
- `field_value_map` – a class that creates `Field-Value`
- `query_pattern` – the template of the source query
- `comment_symbol` – escaping character (metainformation provided for a better context is passed to the output together with the query so it should be commented). If this character allows commenting multiple lines, set the flag `is_multi_line_comment == True`

The class has the following methods:
- The entry point into the process of query rendering is the `generate` method. Query generation process is started for all mappings that match the input query:
    - `generate_prefix` method – a table or an index is generated (depending on the mapping)
    - `generate_query` method – the query's body is generated. The `generate_query` method goes through each token parsed from the source query, and using the `BaseQueryFieldValue` class transforms the `FieldValue` token into a string value that conforms to the rules and standards of the target platform
    - `finalize_query` method – the output query is generated based on `query_pattern` with the metainformation added
- The process ends with the `finalize` method validating the translation output and joining the queries that are identical (that is they match multiple log sources)


### BaseQueryFieldValue Class

The class has the following attributes:
- `details` – the metainformation about the platform (described in the `const.py` file)
- `escape_manager`– a class responsible for processing and escaping special characters

The class has the following methods:
- `__init__` creates a dictionary (map) named `field_value` where a processing method is connected that depends on the operator that was between the field and its value

## Mapping Classes
These classes should be described in the `uncoder-core/app/translator/platforms/<platform_name>/mapping.py` file.

To describe mappings, you need two classes:
- A class that inherits the `BasePlatformMappings` class – responsible for choosing mapping
- A class that inherits the `LogSourceSignature` class – describes the mapping structure.
It's also important to invoke and initialize a class created by inheritance from `BasePlatformMappings` because later it should be connected to the render.

### LogSourceSignature
A class that describes the mapping structure.

The `__init__` method describes tabels/indexes that can be applied for a log source. Also there's an important but optional field `_default_source`, a dictionary that contains the table/index values that can be used for a certain log source at the time of rendering.

The `is_suitable` method is required. It's used to determine the mapping.

### BasePlatformMappings
This class has one required attribute – the name of the directory from which mappings should be taken (all mappings are in `uncoder-core/app/translator/mappings/<platform_name>`). Only the directory name should be indicated.

This class contains two required methods:
- `prepare_log_source_signature` – a method that transforms mappings obtained from the YAML file into objects
- `get_suitable_source_mappings` – a method that contains the conditions for checking for a suitable mapping depending on fields and tables/indexes.

## Escape Manager Class
This class inherits the basic class `EscapeManager`. It contains a required attribute `escape_map`. Depending on the `Value` type (the values searched for in the field) you need to define special characters to be escaped. `Value` types are defined in `uncoder-core/app/translator/core/custom_types/values.py`.

## const.py
The file where the metainformation about the platform and the rule templates (if any) are stored.

## Metainformation
`platform_id` – unique platform identifier  
`group_name` – platform name to be displayed in the platform selection dropdown in the UI  
`platform_name` – the name of the content type to be displayed on the tab (as well as in the sub-menu of the platform)  
`group_id` – the unique identifier of all content types for a platform  
