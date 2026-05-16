"""JSON renderer — structured, machine-readable, fits SIEM/TheHive ingestion."""

from __future__ import annotations

from haak_anvil.core.models import ReportBundle
from haak_anvil.renderers.base import RendererBase


class JsonRenderer(RendererBase):
    extension = "json"

    def __init__(self, *, indent: int = 2) -> None:
        self.indent = indent

    def render(self, bundle: ReportBundle) -> str:
        return bundle.model_dump_json(indent=self.indent, by_alias=False)
