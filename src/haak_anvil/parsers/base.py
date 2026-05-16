"""Parser base class — every tool parser inherits from this."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from haak_anvil.core.engagement import Engagement
from haak_anvil.core.models import ReportBundle


class ParserBase(ABC):
    """Common contract for input parsers.

    Subclass + register a `tool_name` and implement :meth:`parse`.
    """

    tool_name: str = ""

    def __init__(self, engagement: Engagement) -> None:
        if not self.tool_name:
            raise NotImplementedError("Subclass must set class attribute `tool_name`")
        self.engagement = engagement

    @abstractmethod
    def parse(self, path: Path) -> ReportBundle:
        """Parse one input file/dir into a ReportBundle scoped to the engagement."""
        ...

    def parse_many(self, paths: list[Path]) -> ReportBundle:
        """Parse multiple files and merge into a single bundle."""
        if not paths:
            raise ValueError("parse_many called with empty list")
        bundle = self.parse(paths[0])
        for p in paths[1:]:
            bundle = bundle.merge(self.parse(p))
        return bundle
