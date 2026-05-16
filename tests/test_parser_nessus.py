from haak_anvil.core.severity import Severity
from haak_anvil.parsers import NessusParser


def test_nessus_parses_host(nessus_file, engagement):
    bundle = NessusParser(engagement).parse(nessus_file)
    assert len(bundle.assets) == 1
    asset = bundle.assets[0]
    assert asset.address == "10.0.0.10"
    assert asset.hostname == "server01.acme.lan"
    assert "Linux" in (asset.os or "")


def test_nessus_extracts_findings(nessus_file, engagement):
    bundle = NessusParser(engagement).parse(nessus_file)
    titles = [f.title for f in bundle.findings]
    assert any("OpenSSH" in t for t in titles)
    assert any("SSL Self-Signed" in t for t in titles)


def test_nessus_severity_mapped_from_cvss3(nessus_file, engagement):
    bundle = NessusParser(engagement).parse(nessus_file)
    ssh_finding = next(f for f in bundle.findings if "OpenSSH" in f.title)
    # CVSS3 6.5 -> MEDIUM
    assert ssh_finding.severity == Severity.MEDIUM
    assert ssh_finding.cvss is not None
    assert ssh_finding.cvss.score == 6.5
    assert ssh_finding.cvss.version == "3.1"


def test_nessus_critical_from_cvss(nessus_file, engagement):
    bundle = NessusParser(engagement).parse(nessus_file)
    ssl_finding = next(f for f in bundle.findings if "SSL Self-Signed" in f.title)
    assert ssl_finding.severity == Severity.CRITICAL


def test_nessus_extracts_cve_and_cwe(nessus_file, engagement):
    bundle = NessusParser(engagement).parse(nessus_file)
    ssh_finding = next(f for f in bundle.findings if "OpenSSH" in f.title)
    assert "CVE-2020-15778" in ssh_finding.cve
    assert "CWE-78" in ssh_finding.cwe


def test_nessus_extracts_references(nessus_file, engagement):
    bundle = NessusParser(engagement).parse(nessus_file)
    ssh_finding = next(f for f in bundle.findings if "OpenSSH" in f.title)
    assert any("nvd.nist.gov" in r for r in ssh_finding.references)


def test_nessus_severity_breakdown(nessus_file, engagement):
    bundle = NessusParser(engagement).parse(nessus_file)
    counts = bundle.severity_breakdown
    assert counts["critical"] >= 1
    assert counts["medium"] >= 1
