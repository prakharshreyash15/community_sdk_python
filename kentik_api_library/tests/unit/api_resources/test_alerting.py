from http import HTTPStatus
from datetime import datetime

from kentik_api.api_resources.alerting_api import AlertingAPI
from kentik_api.api_calls.api_call import APICallMethods
from kentik_api.public.manual_mitigation import ManualMitigation
from tests.unit.stub_api_connector import StubAPIConnector


def test_create_manual_mitigation_success() -> None:
    # given
    create_response_payload = """
    {
        "response": {
            "result": "OK"
        }
    }"""
    connector = StubAPIConnector(create_response_payload, HTTPStatus.OK)
    alerting_api = AlertingAPI(connector)

    # when
    manual_mitigation = ManualMitigation("192.168.1.0/24", "comment", "1234", "12345", "20")
    created = alerting_api.create_manual_mitigation(manual_mitigation)

    # then
    assert connector.last_url_path == "/alerts/manual-mitigate"
    assert connector.last_method == APICallMethods.POST
    assert connector.last_payload is not None
    assert connector.last_payload["ipCidr"] == "192.168.1.0/24"
    assert connector.last_payload["comment"] == "comment"
    assert connector.last_payload["platformID"] == "1234"
    assert connector.last_payload["methodID"] == "12345"
    assert connector.last_payload["minutesBeforeAutoStop"] == "20"

    assert created is True


def test_get_active_alerts() -> None:
    # given
    create_response_payload = """
    [
        {
            "alarm_id": 82867908,
            "row_type": "Alarm",
            "alarm_state": "ALARM",
            "alert_id": 15094,
            "mitigation_id": null,
            "threshold_id": 76518,
            "alert_key": "443",
            "alert_dimension": "Port_dst",
            "alert_metric": [
                "bits"
            ],
            "alert_value": 2270.4,
            "alert_value2nd": 0,
            "alert_value3rd": 0,
            "alert_match_count": 5,
            "alert_baseline": 769,
            "alert_severity": "minor",
            "baseline_used": 15,
            "learning_mode": 0,
            "debug_mode": 0,
            "alarm_start": "2021-01-19T13:50:00.000Z",
            "alarm_end": "0000-00-00 00:00:00",
            "alarm_last_comment": null,
            "mit_alert_id": 0,
            "mit_alert_ip": "",
            "mit_threshold_id": 0,
            "mit_method_id": 0,
            "args": "",
            "id": 0,
            "policy_id": 15094,
            "policy_name": "test_policy1",
            "alert_key_lookup": "443"
        }
    ]"""
    connector = StubAPIConnector(create_response_payload, HTTPStatus.OK)
    alerting_api = AlertingAPI(connector)

    # when
    alarms = alerting_api.get_active_alerts("2020-10-15T22:15:00", "2021-01-20T09:15:00")

    # then
    assert connector.last_url_path == (
        "/alerts-active/alarms?startTime=2020-10-15T22:15:00&"
        "endTime=2021-01-20T09:15:00&filterBy=None&filterVal=None&"
        "showMitigations=1&showAlarms=1&showMatches=0&learningMode=0"
    )
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    assert len(alarms) == 1
    assert alarms[0].alarm_id == 82867908
    assert alarms[0].alarm_start == datetime(2021, 1, 19, 13, 50, 0, 0)
    assert alarms[0].alarm_end is None


def test_get_alerts_history() -> None:
    create_response_payload = """
    [
        {
            "row_type": "Alarm",
            "old_alarm_state": "CLEAR",
            "new_alarm_state": "ALARM",
            "alert_match_count": "1",
            "alert_severity": "minor",
            "alert_id": 15094,
            "threshold_id": 76518,
            "alarm_id": 82867908,
            "alert_key": "443",
            "alert_dimension": "Port_dst",
            "alert_metric": [
                "bits"
            ],
            "alert_value": 2270.4,
            "alert_value2nd": 0,
            "alert_value3rd": 0,
            "alert_baseline": 769,
            "baseline_used": 15,
            "learning_mode": 0,
            "debug_mode": 0,
            "ctime": "2021-01-19T13:50:00.000Z",
            "alarm_start_time": "2021-01-19 13:50:00",
            "comment": null,
            "mitigation_id": null,
            "mit_method_id": 0,
            "args": "",
            "id": 0,
            "policy_id": 15094,
            "policy_name": "test_policy1",
            "alert_key_lookup": "443"
        }
    ]"""
    connector = StubAPIConnector(create_response_payload, HTTPStatus.OK)
    alerting_api = AlertingAPI(connector)

    # when
    alerts = alerting_api.get_alerts_history("2020-10-15T22:15:00", "2021-01-20T09:15:00", "alert_key", "443")

    # then
    assert connector.last_url_path == (
        "/alerts-active/alerts-history?startTime=2020-10-15T22:15:00&"
        "endTime=2021-01-20T09:15:00&filterBy=alert_key&filterVal=443&sortOrder=None&showMitigations=1&"
        "showAlarms=1&showMatches=0&learningMode=0"
    )
    assert connector.last_method == APICallMethods.GET
    assert connector.last_payload is None

    assert len(alerts) == 1
    assert alerts[0].alarm_id == 82867908
    assert alerts[0].alarm_start_time == datetime(2021, 1, 19, 13, 50, 0, 0)
