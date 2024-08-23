from typing import Optional

from app.translator.core.models.query_container import MetaInfoContainer


class SentinelYamlRuleMetaInfoContainer(MetaInfoContainer):
    def __init__(
        self,
        query_frequency: Optional[str] = None,
        query_period: Optional[str] = None,
        trigger_operator: Optional[str] = None,
        trigger_threshold: Optional[int] = None,
        *args,
        **kwargs,
    ):
        self.query_frequency = query_frequency
        self.query_period = query_period
        self.trigger_operator = trigger_operator
        self.trigger_threshold = trigger_threshold
        super().__init__(*args, **kwargs)
