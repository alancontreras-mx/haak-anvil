from haak_forge.core.severity import Severity
from haak_forge.parsers import NmapParser


def test_nmap_parses_hosts(nmap_xml, engagement):
    bundle = NmapParser(engagement).parse(nmap_xml)
    addresses = [a.address for a in bundle.assets]
    assert "10.0.0.10" in addresses
    assert "10.0.0.20" in addresses
    assert len(bundle.assets) == 2


def test_nmap_skips_closed_ports(nmap_xml, engagement):
    bundle = NmapParser(engagement).parse(nmap_xml)
    server01 = next(a for a in bundle.assets if a.address == "10.0.0.10")
    port_numbers = [p.number for p in server01.ports]
    assert 22 in port_numbers
    assert 80 in port_numbers
    assert 443 in port_numbers
    assert 3389 not in port_numbers  # closed


def test_nmap_extracts_service_metadata(nmap_xml, engagement):
    bundle = NmapParser(engagement).parse(nmap_xml)
    server01 = next(a for a in bundle.assets if a.address == "10.0.0.10")
    ssh = next(p for p in server01.ports if p.number == 22)
    assert ssh.service is not None
    assert ssh.service.product == "OpenSSH"
    assert ssh.service.version == "8.2p1"


def test_nmap_emits_info_finding_per_open_port(nmap_xml, engagement):
    bundle = NmapParser(engagement).parse(nmap_xml)
    # 3 open on .10 + 1 on .20 = 4
    assert len(bundle.findings) == 4
    assert all(f.severity == Severity.INFO for f in bundle.findings)
    assert all(f.tool == "nmap" for f in bundle.findings)


def test_nmap_finding_ids_are_stable_and_unique(nmap_xml, engagement):
    bundle = NmapParser(engagement).parse(nmap_xml)
    ids = [f.id for f in bundle.findings]
    assert len(ids) == len(set(ids))
