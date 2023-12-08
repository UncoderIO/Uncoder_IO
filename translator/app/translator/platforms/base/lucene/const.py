
COMPARISON_OPERATORS_MAP = {
    ":[* TO": {
        "replace": [":\[\*\sTO"],
        "default_op": "<="
    },
    ":[": {
        "replace": [":\[", "TO\s\*"],
        "default_op": ">="
    },
}
