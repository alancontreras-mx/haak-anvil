# Changelog

All notable changes to Haak Anvil will be documented in this file. The format
is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this
project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned for v0.2
- Burp Suite XML parser
- Nuclei JSON parser
- OWASP ZAP JSON parser
- CVE enrichment via NVD 2.0 API + EPSS scoring
- HTML template variants (executive / technical / pretty-print)
- PDF renderer via WeasyPrint
- DOCX renderer via python-docx
- AI executive summary (Claude API)
- Engagement YAML template generator
- Cache layer for NVD lookups

## [0.1.0] — 2026-05-15

### Added
- Initial release.
- Core data models (`Engagement`, `Asset`, `Port`, `Service`, `Finding`, `CVSS`, `Severity`, `ReportBundle`)
- Severity normalization helpers (CVSS → Severity, Nessus risk_factor → Severity)
- Nmap XML parser (Nmap 7.x compatible, defusedxml)
- Nessus v2 .nessus parser (CVSS v3 preferred, CVE/CWE extraction from tags + free text)
- Renderers: JSON (machine), Markdown (human), HTML (Jinja2 + Tailwind CDN)
- CLI: `haak-anvil nmap | nessus | merge | version`
- ReportBundle merge across multiple tools on same engagement
- Test suite (pytest, fixtures for Nmap + Nessus samples)
- GitHub Actions CI (Linux/Mac/Windows × Python 3.10/3.11/3.12)
- Apache 2.0 license
- README + CHANGELOG + .gitignore

### Authors
- Alan Contreras (`@HaakConsulting` / contacto@haak.com.mx)

[Unreleased]: https://github.com/alancontreras-mx/haak-anvil/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/alancontreras-mx/haak-anvil/releases/tag/v0.1.0
