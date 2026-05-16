from haak_forge.renderers.base import RendererBase
from haak_forge.renderers.html import HtmlRenderer
from haak_forge.renderers.json_renderer import JsonRenderer
from haak_forge.renderers.markdown import MarkdownRenderer

__all__ = ["HtmlRenderer", "JsonRenderer", "MarkdownRenderer", "RendererBase"]


def get_renderer(format_name: str) -> type[RendererBase]:
    """Factory: 'json' / 'md' / 'html' -> class."""
    table: dict[str, type[RendererBase]] = {
        "json": JsonRenderer,
        "md": MarkdownRenderer,
        "markdown": MarkdownRenderer,
        "html": HtmlRenderer,
    }
    fmt = format_name.lower()
    if fmt not in table:
        raise ValueError(
            f"Unknown format {format_name!r}; choose from {sorted(table)}"
        )
    return table[fmt]
