# Haak Forge — Architecture

## Pipeline

```
   ┌───────────┐     ┌────────────┐     ┌─────────────┐     ┌────────────┐
   │ Raw scan  │────▶│   Parser   │────▶│  Enricher   │────▶│  Renderer  │────▶ report.{json,md,html}
   │ (XML/JSON)│     │ (per tool) │     │ (CVE,EPSS)  │     │ (per fmt)  │
   └───────────┘     └────────────┘     └─────────────┘     └────────────┘
                            │                  │                  │
                            └───── ReportBundle (pydantic) ──────┘
```

All stages exchange a single typed object: `ReportBundle`. This means a renderer
never depends on a parser, and vice versa.

## Adding a new parser

1. Subclass `ParserBase`, set `tool_name = "yourtool"`.
2. Implement `parse(path: Path) -> ReportBundle`.
3. Register in `parsers/__init__.py` and add a CLI command in `cli.py`.
4. Drop a sample fixture in `tests/fixtures/`.
5. Write tests in `tests/test_parser_yourtool.py`.

Pattern: tool-specific severity strings should be mapped to the canonical
`Severity` enum via a helper in `core/severity.py` to keep behavior consistent.

## Adding a new renderer

1. Subclass `RendererBase`, set `extension = "..."`.
2. Implement `render(bundle: ReportBundle) -> str`.
3. Register in `renderers/__init__.py` and add to the `get_renderer` factory.

## Merging multi-tool reports

`ReportBundle.merge(other)` deduplicates assets by address and concatenates
findings. Used by the CLI `merge` command to combine, for example, a Nmap
recon pass with a Nessus authenticated scan in a single deliverable.

## Future: enrichers

Enrichers take a bundle and return an annotated bundle. Currently a stub. v0.2
will include:

- **CveEnricher**: fetch NVD 2.0 data for every CVE ID, fill missing CVSS/CWE.
- **EpssEnricher**: pull EPSS probability from first.org, surface "most likely
  to be exploited" findings to the top of the report.
- **ExploitAvailabilityEnricher**: check ExploitDB / GitHub PoC presence.
