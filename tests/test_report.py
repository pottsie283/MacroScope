from macroscope.report import Report

def test_report_json():
    findings = {"test": "value"}
    report = Report(findings)
    json_str = report.to_json()
    assert '"test": "value"' in json_str
    assert '"risk_score":' in json_str
