"""Renderer base class — every output format inherits from this."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from haak_forge.core.models import ReportBundle


class RendererBase(ABC):
    """Render a ReportBundle into a string and/or write to disk."""

    extension: str = ""

    @abstractmethod
    def render(self, bundle: ReportBundle) -> str:
        """Return the rendered report content."""
        ...

    def write(self, bundle: ReportBundle, path: Path | str) -> Path:
        """Render and write to disk. Returns the written path."""
        path = Path(path)
        if path.is_dir() or path.suffix == "":
            path = path / f"{bundle.engagement.id}.{self.extension}"
        content = self.render(bundle)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path
