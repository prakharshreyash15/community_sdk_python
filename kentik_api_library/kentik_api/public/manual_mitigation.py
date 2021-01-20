from typing import Optional, List
from dataclasses import dataclass
from datetime import datetime


@dataclass()
class ManualMitigation:
    ipCidr: str
    comment: Optional[str]
    platformID: str
    methodID: str
    minutesBeforeAutoStop: str


@dataclass
class Alarm:
    alarm_id: int
    row_type: str
    alarm_state: str
    alert_id: int
    mitigation_id: Optional[int]
    threshold_id: int
    alert_key: str
    alert_dimension: str
    alert_metric: List[str]
    alert_value: float
    alert_value2nd: float
    alert_value3rd: float
    alert_match_count: int
    alert_baseline: int
    alert_severity: str
    baseline_used: int
    learning_mode: int
    debug_mode: bool
    alarm_start: datetime
    alarm_end: Optional[datetime]
    alarm_last_comment: Optional[str]
    mit_alert_id: int
    mit_alert_ip: str
    mit_threshold_id: int
    args: str
    id: int
    policy_id: int
    policy_name: str
    alert_key_lookup: str


@dataclass
class HiscoricalAlert:
    row_type: str
    old_alarm_state: str
    new_alarm_state: str
    alert_match_count: str
    alert_severity: str
    alert_id: int
    threshold_id: int
    alarm_id: int
    alert_key: str
    alert_dimension: str
    alert_metric: List[str]
    alert_value: float
    alert_value2nd: int
    alert_value3rd: int
    alert_baseline: int
    baseline_used: int
    learning_mode: int
    debug_mode: int
    ctime: datetime
    alarm_start_time: datetime
    comment: Optional[str]
    mitigation_id: Optional[int]
    mit_method_id: int
    args: str
    id: int
    policy_id: int
    policy_name: str
    alert_key_lookup: str
