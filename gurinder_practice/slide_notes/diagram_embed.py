"""GitHub-friendly diagram embeds and SVG display sizing."""
from __future__ import annotations

import re
import sys
from html import escape
from pathlib import Path

DIAGRAM_DISPLAY_WIDTH = 220
LAYOUT_SCALE = 0.44

SVG_OPEN_RE = re.compile(
    r"<svg\b(?P<before>[^>]*)\bviewBox=\"0 0 (?P<vw>\d+(?:\.\d+)?) (?P<vh>\d+(?:\.\d+)?)\"(?P<after>[^>]*)>",
    re.DOTALL,
)
IMG_WIDTH_RE = re.compile(r'(<img\b[^>]*\bwidth=")(\d+)(")', re.IGNORECASE)
SVG_LINK_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+\.svg)\)")


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

    md = SVG_LINK_RE.sub(repl, md)
    md = re.sub(r"→ \[([^\]]*)\]\(([^)]+\.svg)\)", repl, md)
    return md


def update_markdown_diagrams(md: str, base_dir: Path, max_width: int = DIAGRAM_DISPLAY_WIDTH) -> str:
    def repl(match: re.Match[str]) -> str:
        rel = match.group(2)
        svg_path = base_dir / rel.replace("/", "\\") if "\\" not in rel else base_dir / rel
        if not svg_path.exists():
            svg_path = base_dir / Path(rel).name
        width = max_width
        if svg_path.exists():
            width = display_width_for_svg(svg_path.read_text(encoding="utf-8"), max_width)
        return format_diagram_embed(match.group(1), rel, width)

    md = SVG_LINK_RE.sub(repl, md)

    def img_repl(match: re.Match[str]) -> str:
        tag = match.group(0)
        src_m = re.search(r'src="([^"]+\.svg)"', tag, re.IGNORECASE)
        if not src_m:
            return tag
        rel = src_m.group(1)
        svg_path = base_dir / rel
        if not svg_path.exists():
            return tag
        width = display_width_for_svg(svg_path.read_text(encoding="utf-8"), max_width)
        return IMG_WIDTH_RE.sub(rf"\g<1>{width}\3", tag, count=1)

    return re.sub(r"<img\b[^>]*>", img_repl, md, flags=re.IGNORECASE)


def resync_svg_directory(directory: Path, max_width: int = DIAGRAM_DISPLAY_WIDTH) -> int:
    count = 0
    for path in sorted(directory.glob("*.svg")):
        original = path.read_text(encoding="utf-8")
        updated = add_svg_display_size(original, max_width)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            count += 1
    return count


def resync_all(root: Path | None = None) -> None:
    root = root or Path(__file__).resolve().parent
    repo = root.parent

    svg_dirs = [
        root / "day1_diagrams",
        root / "day2_diagrams",
        repo / "lab 1.1" / "diagrams",
    ]
    md_files = [
        root / "day1_study_notes.md",
        root / "day2_study_notes.md",
        root / "day1_speaker_notes.md",
        root / "day2_speaker_notes.md",
    ]

    for directory in svg_dirs:
        if directory.is_dir():
            n = resync_svg_directory(directory)
            print(f"{directory.name}: updated {n} SVG(s)")

    for path in md_files:
        if not path.exists():
            continue
        original = path.read_text(encoding="utf-8")
        updated = update_markdown_diagrams(original, root, DIAGRAM_DISPLAY_WIDTH)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            print(f"{path.name}: updated diagram embeds")


def main() -> None:
    resync_all(Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else None)


if __name__ == "__main__":
    main()
