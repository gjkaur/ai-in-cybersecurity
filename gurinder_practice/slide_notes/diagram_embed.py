"""GitHub-friendly diagram embeds and SVG display sizing."""
from __future__ import annotations

import re
from html import escape

DIAGRAM_DISPLAY_WIDTH = 480
LAYOUT_SCALE = 0.88

SVG_OPEN_RE = re.compile(
    r"<svg\b(?P<before>[^>]*)\bviewBox=\"0 0 (?P<vw>\d+(?:\.\d+)?) (?P<vh>\d+(?:\.\d+)?)\"(?P<after>[^>]*)>",
    re.DOTALL,
)


def format_diagram_embed(alt: str, path: str, width: int = DIAGRAM_DISPLAY_WIDTH) -> str:
    alt_esc = escape(alt.strip() or "Diagram", quote=True)
    return f'\n<img src="{path}" width="{width}" alt="{alt_esc}">\n'


def add_svg_display_size(svg: str, max_width: int = DIAGRAM_DISPLAY_WIDTH) -> str:
    match = SVG_OPEN_RE.search(svg)
    if not match:
        return svg
    w, h = float(match.group("vw")), float(match.group("vh"))
    display_w = min(w, max_width)
    display_h = max(1, round(h * display_w / w))

    before = re.sub(r'\swidth="[^"]*"', "", match.group("before"))
    before = re.sub(r'\sheight="[^"]*"', "", before)
    after = re.sub(r'\swidth="[^"]*"', "", match.group("after"))
    after = re.sub(r'\sheight="[^"]*"', "", after)

    new_open = (
        f'<svg{before}viewBox="0 0 {match.group("vw")} {match.group("vh")}" '
        f'width="{int(display_w)}" height="{int(display_h)}"{after}>'
    )
    return svg[: match.start()] + new_open + svg[match.end() :]


def convert_svg_markdown(md: str, width: int = DIAGRAM_DISPLAY_WIDTH) -> str:
    def repl(match: re.Match[str]) -> str:
        return format_diagram_embed(match.group(1), match.group(2), width)

    md = re.sub(r"!\[([^\]]*)\]\(([^)]+\.svg)\)", repl, md)
    md = re.sub(r"→ \[([^\]]*)\]\(([^)]+\.svg)\)", repl, md)
    return md
