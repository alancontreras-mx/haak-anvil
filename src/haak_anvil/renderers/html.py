"""HTML renderer — Jinja2 + Tailwind via CDN. Single-file, no build."""

from __future__ import annotations

from jinja2 import Environment, FileSystemLoader, select_autoescape

from haak_anvil.core.models import ReportBundle
from haak_anvil.core.severity import Severity
from haak_anvil.renderers.base import RendererBase

_TEMPLATES_DIR = __file__.replace("renderers/html.py", "templates/html").replace(
    "renderers\\html.py", "templates\\html"
)

_SEV_CLASS = {
    Severity.CRITICAL: "bg-red-600 text-white",
    Severity.HIGH: "bg-orange-500 text-white",
    Severity.MEDIUM: "bg-yellow-400 text-black",
    Severity.LOW: "bg-blue-500 text-white",
    Severity.INFO: "bg-gray-400 text-white",
}


class HtmlRenderer(RendererBase):
    extension = "html"

    def __init__(self, template_name: str = "default.html.j2") -> None:
        self.env = Environment(
            loader=FileSystemLoader(_TEMPLATES_DIR),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        self.env.filters["sev_class"] = lambda s: _SEV_CLASS.get(s, "bg-gray-300")
        self.template_name = template_name

    def render(self, bundle: ReportBundle) -> str:
        template = self.env.get_template(self.template_name)
        return template.render(
            bundle=bundle,
            engagement=bundle.engagement,
            findings=bundle.findings_sorted(),
            assets=bundle.assets,
            breakdown=bundle.severity_breakdown,
            Severity=Severity,
        )
