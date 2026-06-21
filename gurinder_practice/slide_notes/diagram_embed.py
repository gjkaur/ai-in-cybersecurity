"""GitHub-friendly diagram embed sizing for study notes."""
from __future__ import annotations

import re
from html import escape

DIAGRAM_DISPLAY_WIDTH = 420
SVG_OPEN_RE = re.compile(
    r'<svg\b(?P<before>[^>]*)\bviewBox="0 0 (?P<vw>\d+(?:\.\d+)?) (?P<vh>\d+(?:\.\d+)?)"(?P<after>[^>]*)>',
    re.DOTALL,
)
IMG_WIDTH_RE = re.compile(r'(<img\b[^>]*\bwidth=")(\d+)(")', re.IGNORECASE)


def format_diagram_embed(alt: str, path: str, width: int = DIAGRAM_DISPLAY_WIDTH) -> str:
    alt_esc = escape(alt.strip() or "Diagram", quote=True)
    return f'\n<img src="{path}" width="{width}" alt="{alt_esc}">\n'


def svg_viewbox_width(svg: str) -> float | None:
    match = SVG_OPEN_RE.search(svg)
    if not match:
        return None
    return float(match.group("vw"))


def display_width_for_svg(svg: str, max_width: int = DIAGRAM_DISPLAY_WIDTH) -> int:
    vb = svg_viewbox_width(svg)
    if vb is None:
        return max_width
    return int(min(vb, max_width))


def update_markdown_diagram_widths(md: str, base_dir, max_width: int = DIAGRAM_DISPLAY_WIDTH) -> str:
    from pathlib import Path

    base = Path(base_dir)

    def repl(match: re.Match[str]) -> str:
        before, width, after = match.group(1), match.group(2), match.group(3)
        src_m = re.search(r'src="([^"]+)"', match.group(0), re.I)
        if not src_m:
            return match.group(0)
        svg_path = base / src_m.group(1).replace("/", "\\")
        if not svg_path.exists():
            svg_path = base / Path(src_m.group(1)).name
        new_w = max_width
        if svg_path.exists():
            new_w = display_width_for_svg(svg_path.read_text(encoding="utf-8"), max_width)
        return f'{before}{new_w}{after}'

    return IMG_WIDTH_RE.sub(repl, md)
