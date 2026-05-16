"""CVE enrichment via NVD 2.0 API.

Stub for v0.1 — full implementation expands in Fase 2 with:
  - NVD JSON 2.0 fetch
  - EPSS score from first.org
  - Exploit availability check (ExploitDB, GitHub PoCs)
  - Local cache with TTL
"""

from __future__ import annotations

import httpx

from haak_forge.core.models import ReportBundle

NVD_API = "https://services.nvd.nist.gov/rest/json/cves/2.0"


class CveEnricher:
    """Placeholder — currently a no-op that returns the bundle unchanged.

    Wire in Fase 2:
      - Async fetch per unique CVE in findings
      - Annotate with CVSS v3.1 if missing
      - Add EPSS percentile
      - Cache in ~/.haak-forge/cache/cve/
    """

    def __init__(self, *, timeout: float = 10.0, api_key: str | None = None) -> None:
        self.timeout = timeout
        self.api_key = api_key

    async def enrich(self, bundle: ReportBundle) -> ReportBundle:
        # TODO Fase 2
        return bundle

    @staticmethod
    async def _fetch_cve(cve_id: str, *, client: httpx.AsyncClient) -> dict | None:
        try:
            r = await client.get(NVD_API, params={"cveId": cve_id})
            r.raise_for_status()
            data = r.json()
            vulns = data.get("vulnerabilities", [])
            return vulns[0] if vulns else None
        except (httpx.HTTPError, ValueError):
            return None
