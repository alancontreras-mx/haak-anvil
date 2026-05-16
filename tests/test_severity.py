from haak_forge.core.severity import CVSS, Severity, severity_from_cvss


def test_severity_numeric_order():
    assert Severity.INFO.numeric < Severity.LOW.numeric
    assert Severity.LOW.numeric < Severity.MEDIUM.numeric
    assert Severity.MEDIUM.numeric < Severity.HIGH.numeric
    assert Severity.HIGH.numeric < Severity.CRITICAL.numeric


def test_severity_labels_es():
    assert Severity.CRITICAL.label_es == "Crítica"
    assert Severity.INFO.label_es == "Informativo"


def test_cvss_to_severity_thresholds():
    assert severity_from_cvss(9.8) == Severity.CRITICAL
    assert severity_from_cvss(9.0) == Severity.CRITICAL
    assert severity_from_cvss(8.9) == Severity.HIGH
    assert severity_from_cvss(7.0) == Severity.HIGH
    assert severity_from_cvss(6.9) == Severity.MEDIUM
    assert severity_from_cvss(4.0) == Severity.MEDIUM
    assert severity_from_cvss(3.9) == Severity.LOW
    assert severity_from_cvss(0.1) == Severity.LOW
    assert severity_from_cvss(0.0) == Severity.INFO


def test_cvss_validates_vector_prefix():
    import pytest as _pt
    CVSS(score=7.5, vector="CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H")
    with _pt.raises(ValueError):
        CVSS(score=5.0, vector="garbage")


def test_cvss_score_bounds():
    import pytest as _pt
    CVSS(score=0.0)
    CVSS(score=10.0)
    with _pt.raises(ValueError):
        CVSS(score=10.1)
    with _pt.raises(ValueError):
        CVSS(score=-0.1)
