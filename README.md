# Haak Anvil

> Modern, multi-format pentest report generator. Mexican-built, professional-grade.

[![License: Apache-2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org)
[![Status: Alpha](https://img.shields.io/badge/status-alpha-orange)]()

**Haak Anvil** turns raw scanner output (Nmap, Nessus, and many more coming) into
**professional, multi-format pentest reports** with consistent severity scoring,
engagement-scoped metadata, CVE/CWE enrichment, and templates ready to ship to a
client.

Built for offensive security teams who deliver **real engagements**, not just
PDFs full of bullet points.

---

## Why another report tool?

Existing tools either:

- Output Excel-only with no engagement context.
- Hard-code a single tool's format and break when you switch scanners.
- Are unmaintained Python 2 relics.
- Hide everything behind a SaaS paywall.

Haak Anvil is:

- **Modern Python 3.10+** (type-hinted, pydantic v2, async-ready).
- **Multi-tool first**: Nmap and Nessus today, Burp / Nuclei / ZAP / sqlmap / Subfinder next.
- **Multi-format output**: JSON (machine), Markdown (humans), HTML (clients), PDF + DOCX coming.
- **Engagement-scoped**: every report is tied to a YAML-defined engagement (client, scope, dates, methodology, analyst).
- **CVE/CWE-aware**: pulls IDs from tag fields and free text, ready for NVD/EPSS enrichment (v0.2).
- **Apache 2.0**: use it commercially, no obligations.

---

## Quickstart

```bash
git clone https://github.com/alancontreras-mx/haak-anvil.git
cd haak-anvil
python -m pip install -e .
```

### Parse an Nmap scan and emit HTML

```bash
nmap -sV -oX out.xml 10.0.0.0/24
haak-anvil nmap out.xml --format html --output report.html
```

### Parse a Nessus export

```bash
haak-anvil nessus client.nessus --format md --output report.md
```

### Scoped engagement

Create `engagement.yaml`:

```yaml
id: HK-2026-001
client:
  name: Acme Corp
  contact: ciso@acme.example
scope: "External perimeter + corporate WLAN"
methodology: PTES
period:
  start: 2026-05-10
  end:   2026-05-20
analyst: Alan Contreras
language: es-MX
```

Then:

```bash
haak-anvil nmap out.xml -e engagement.yaml -f html -o reports/
haak-anvil nessus client.nessus -e engagement.yaml -f json -o reports/
```

### Merge multi-tool results

```bash
haak-anvil nmap out.xml -e engagement.yaml -f json -o reports/nmap.json
haak-anvil nessus client.nessus -e engagement.yaml -f json -o reports/nessus.json
haak-anvil merge reports/nmap.json reports/nessus.json -e engagement.yaml -f html -o reports/final.html
```

---

## Architecture

```
haak_anvil/
├── core/         # Engagement, Asset, Port, Finding, CVSS, Severity, ReportBundle
├── parsers/      # ParserBase + nmap, nessus  (burp, nuclei, zap, sqlmap... v0.2)
├── renderers/    # RendererBase + json, markdown, html  (pdf, docx... v0.2)
├── enrichers/    # CVE/EPSS enrichment via NVD 2.0 API (stub v0.1, full v0.2)
├── templates/    # Jinja2 HTML templates
└── cli.py        # Typer CLI
```

Every parser maps tool-specific output into a unified `ReportBundle`. Every
renderer consumes a `ReportBundle` and emits a format. Adding a new tool is a
~150-line module that subclasses `ParserBase`.

---

## Supported tools (v0.1)

| Tool        | Status | Notes                                              |
|-------------|--------|----------------------------------------------------|
| Nmap        | ✅     | XML output (`-oX`); 7.x tested                    |
| Nessus      | ✅     | `.nessus` v2 export; CVSS v3 preferred over v2    |
| Burp Suite  | 🚧 v0.2 | XML export                                       |
| Nuclei      | 🚧 v0.2 | JSONL output                                     |
| OWASP ZAP   | 🚧 v0.2 | JSON/XML reports                                 |
| sqlmap      | 🚧 v0.2 | Output dir parsing                               |
| Subfinder   | 🚧 v0.2 | JSON output                                      |
| Gowitness   | 🚧 v0.2 | SQLite asset enrichment                          |

---

## Output formats (v0.1)

| Format      | Status | Use case                                  |
|-------------|--------|-------------------------------------------|
| JSON        | ✅     | Machine ingest (TheHive, SIEM, custom)    |
| Markdown    | ✅     | GitHub wikis, internal docs               |
| HTML        | ✅     | Client deliverable (Tailwind CDN, single file) |
| PDF         | 🚧 v0.2 | Printable, WeasyPrint                    |
| DOCX        | 🚧 v0.2 | Editable client deliverable              |

---

## Roadmap

- **v0.2** (target Q3-2026): Burp + Nuclei + ZAP + sqlmap parsers, CVE/EPSS enrichment, PDF + DOCX renderers, HTML template variants.
- **v0.3**: Optional FastAPI + HTMX web UI, plugin system via entry points, multi-language report templates (es-MX / en-US / pt-BR).
- **v0.4**: AI-powered executive summary (Claude API), TheHive / Wazuh / MISP push integrations, chain-of-custody signing (Ed25519).

See [CHANGELOG.md](CHANGELOG.md) for full release history.

---

## Development

```bash
python -m pip install -e ".[dev]"
ruff check src tests
pytest --cov=haak_anvil --cov-report=term-missing
```

PRs welcome. Open an issue first for big changes.

---

## License

Apache License 2.0. See [LICENSE](LICENSE).

---

## Author

**Alan Contreras** — CEO & Co-Founder, [Haak Cybersecurity Consulting](https://haak.com.mx)
México · [contacto@haak.com.mx](mailto:contacto@haak.com.mx) · [LinkedIn](https://mx.linkedin.com/in/alan-contreras-)

Built in the tradition of pentest report tooling (dradis-ce, faraday-ng, secutils),
rewritten from scratch with modern Python for 2026 workflows.
