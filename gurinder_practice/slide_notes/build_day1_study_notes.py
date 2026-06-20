"""Build refined Day 1 slide notes: single organized file + text-diagram → SVG."""
from __future__ import annotations

import re
import shutil
from pathlib import Path

from diagram_embed import DIAGRAM_DISPLAY_WIDTH, LAYOUT_SCALE, add_svg_display_size, format_diagram_embed

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "day1_notes.md"
DIAGRAMS = ROOT / "day1_diagrams"
DIAGRAM_REL = "day1_diagrams"
OUTPUT = ROOT / "day1_study_notes.md"

S = LAYOUT_SCALE


def sc(n: int | float) -> int:
    return max(1, int(round(n * S)))


FONT = "Arial, Helvetica, sans-serif"
MONO = "Consolas, monospace"
C = {
    "bg": "#F8FAFC",
    "panel": "#FFFFFF",
    "border": "#E2E8F0",
    "text": "#0F172A",
    "muted": "#64748B",
    "blue": "#2563EB",
    "blue_bg": "#EFF6FF",
    "blue_border": "#93C5FD",
    "green": "#16A34A",
    "green_bg": "#ECFDF5",
    "green_border": "#86EFAC",
    "amber": "#D97706",
    "slate": "#475569",
    "aws": "#FF9900",
}

COURSE_BLOCKS = [
    {
        "name": "Foundations",
        "slides": "6–10",
        "topics": [
            "What is Cybersecurity?",
            "The CIA Triad",
            "The Modern Threat Landscape",
            "Cloud Computing and the New Perimeter",
            "Shared Responsibility Model (Deep Dive)",
        ],
    },
    {
        "name": "AWS & EC2",
        "slides": "11–23",
        "topics": [
            "AWS and Cloud Infrastructure",
            "AWS Regions, Availability Zones, IAM, VPC, and EC2",
            "IAM Roles, Least Privilege, EC2, VPC and S3 Access",
            "Virtual Machines and EC2 Instances",
            "Launching EC2 Instances Safely",
            "SSH (Secure Shell)",
            "SSH Key-Based Authentication",
            "Navigating the Linux Filesystem",
            "Linux File Permissions",
            "SetUID Binaries and Privilege Risk",
            "Finding and Investigating SetUID Binaries",
            "Security Groups as Firewalls",
            "Running and Securing a Web Service",
        ],
    },
    {
        "name": "SOC & Detection",
        "slides": "31–44",
        "topics": [
            "The SOC Analyst Role",
            "The Cyber Kill Chain",
        ],
    },
    {
        "name": "MITRE ATT&CK & Attacks",
        "slides": "31–44",
        "topics_prefix": [
            "MITRE ATT&CK FRAMEWORK",
            "BRUTE FORCE AND CREDENTIAL ATTACKS",
            "PRIVILEGE ESCALATION",
            "WHY LOGS ARE THE FOUNDATION",
            "LINUX LOGGING",
            "COLLECTING SSH EVIDENCE",
            "EVIDENCE AND THE ANALYST WORKFLOW",
            "RISK SCORING FUNDAMENTALS",
        ],
    },
    {
        "name": "AI in Security",
        "slides": "52–65",
        "topics_prefix": [
            "AI Limitations",
            "Security-Safe AI",
            "Common Security Tasks AI",
        ],
    },
    {
        "name": "CSPM & AWS Security",
        "slides": "73–96",
        "topics_prefix": [
            "Cloud Security Posture Management",
            "AWS Security Services Overview",
            "AWS Security Hub",
            "IAM Access Analyzer",
            "MFA Options",
            "S3 Bucket Security",
            "AWS CloudTrail",
            "Security Findings Baseline",
        ],
    },
]


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def slugify(text: str) -> str:
    text = re.sub(r"^Slide Topic:\s*", "", text)
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "-", text).strip("-")[:80]


def is_arrow_line(line: str) -> bool:
    s = line.strip()
    return s in {"↓", "↑", "→", "←", "|", "│", "▼", "▲"}


def is_separator(line: str) -> bool:
    s = line.strip()
    return len(s) >= 4 and all(c in "-=_*" for c in s)


BOX_DRAWING = set("┌┐└┘│─┼┴┬├┤▼▲→←↓↑▶◀")


def has_box_drawing(text: str) -> bool:
    return any(c in BOX_DRAWING for c in text)


def is_diagram_block(text: str, context: str) -> bool:
    ctx = context.lower()
    in_diagram_section = any(
        k in ctx
        for k in (
            "whiteboard diagram",
            "visual diagram",
            "visual example",
            "visual understanding",
            "think of it as",
            "draw:",
            "draw this",
            "example workflow",
            "example soc dashboard",
            "how components work",
        )
    )
    lines = [ln.strip() for ln in text.strip().splitlines() if ln.strip()]
    if len(lines) < 2:
        return False

    if has_box_drawing(text):
        return True

    arrow_lines = sum(is_arrow_line(ln) for ln in lines)
    sep_lines = sum(is_separator(ln) for ln in lines)
    pipe_rows = sum(1 for ln in lines if "|" in ln and len(ln.split("|")) >= 3)

    if in_diagram_section:
        return True
    if sep_lines >= 1 and len(lines) >= 3:
        return True
    if arrow_lines >= 2:
        return True
    if pipe_rows >= 1:
        return True
    if arrow_lines >= 1 and len(lines) >= 4:
        return True
    return False


def is_decorative_line(line: str) -> bool:
    s = line.strip()
    if is_separator(s):
        return True
    return bool(re.fullmatch(r"[\s|]+", s))


def split_columns(line: str) -> list[str] | None:
    if is_decorative_line(line):
        return None
    if "|" in line:
        parts = [p.strip() for p in line.split("|") if p.strip()]
        if len(parts) >= 2:
            return parts
    parts = [p.strip() for p in re.split(r"\s{2,}", line.strip()) if p.strip()]
    if len(parts) >= 2 and not all(len(p) <= 1 for p in parts):
        return parts
    return None


def wrap_label(text: str, max_chars: int = 20) -> list[str]:
    words = text.split()
    if not words:
        return [text]
    lines: list[str] = []
    current: list[str] = []
    for w in words:
        trial = " ".join(current + [w])
        if len(trial) <= max_chars:
            current.append(w)
        else:
            if current:
                lines.append(" ".join(current))
            current = [w]
    if current:
        lines.append(" ".join(current))
    return lines or [text]


def box_dims(label: str, min_w: int = 84, pad: int = 24) -> tuple[int, int]:
    wrapped = wrap_label(label)
    w = max(sc(min_w), max(len(line) for line in wrapped) * sc(6) + sc(pad))
    h = sc(24) + len(wrapped) * sc(14)
    return w, h


def render_box(x: int, y: int, w: int, h: int, label: str, fill: str, stroke: str) -> str:
    wrapped = wrap_label(label, max_chars=max(18, w // 7))
    inner = (
        f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="1.8" filter="url(#sh)"/>\n'
    )
    start_y = y + sc(14) + (h - len(wrapped) * sc(14)) // 2
    for i, line in enumerate(wrapped):
        inner += (
            f'  <text x="{x + w // 2}" y="{start_y + i * sc(14)}" text-anchor="middle" '
            f'font-family="{FONT}" font-size="{sc(10)}" font-weight="600" fill="{C["text"]}">{esc(line)}</text>\n'
        )
    return inner


def render_arrow_down(x: int, y: int, height: int = 20) -> str:
    y2 = y + height
    return (
        f'  <line x1="{x}" y1="{y}" x2="{x}" y2="{y2 - 6}" stroke="{C["slate"]}" '
        f'stroke-width="2" marker-end="url(#m-slate)"/>\n'
    )


def render_tree_branches(
    cx: int, y: int, root_w: int, children: list[str], fill: str, stroke: str
) -> tuple[str, int, int]:
    """Draw root fan-out to a row of child boxes. Returns (svg, new_y, row_width)."""
    child_sizes = [box_dims(c, min_w=96) for c in children]
    gap = sc(12)
    row_w = sum(w for w, _ in child_sizes) + gap * (len(children) - 1)
    row_h = max(h for _, h in child_sizes)
    start_x = cx - row_w // 2
    stem = sc(14)
    inner = render_arrow_down(cx, y, stem)
    y += stem
    bar_y = y + sc(6)
    inner += (
        f'  <line x1="{start_x}" y1="{bar_y}" x2="{start_x + row_w}" y2="{bar_y}" '
        f'stroke="{C["slate"]}" stroke-width="2"/>\n'
    )
    x = start_x
    box_y = bar_y + sc(12)
    for i, (child, (cw, ch)) in enumerate(zip(children, child_sizes)):
        child_cx = x + cw // 2
        inner += (
            f'  <line x1="{child_cx}" y1="{bar_y}" x2="{child_cx}" y2="{box_y}" '
            f'stroke="{C["slate"]}" stroke-width="2"/>\n'
        )
        inner += render_box(x, box_y, cw, ch, child, fill, stroke)
        x += cw + gap
    return inner, box_y + row_h, row_w


def render_row(labels: list[str], cx: int, y: int, fill: str, stroke: str) -> tuple[str, int, int]:
    sizes = [box_dims(lbl, min_w=84) for lbl in labels]
    gap = sc(12)
    row_w = sum(w for w, _ in sizes) + gap * (len(labels) - 1)
    row_h = max(h for _, h in sizes)
    x = cx - row_w // 2
    inner = ""
    for lbl, (w, h) in zip(labels, sizes):
        inner += render_box(x, y, w, h, lbl, fill, stroke)
        x += w + gap
    return inner, y + row_h, row_w


def svg_defs() -> str:
    return """  <defs>
    <filter id="sh" x="-12%" y="-12%" width="124%" height="124%">
      <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#0F172A" flood-opacity="0.1"/>
    </filter>
    <marker id="m-slate" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M1 2 L9 5 L1 8" fill="none" stroke="#475569" stroke-width="1.8" stroke-linecap="round"/>
    </marker>
  </defs>
"""


def render_group_panel(items: list[str], cx: int, y: int) -> tuple[str, int, int]:
    """Stack items in a bordered panel (section header + bullet list)."""
    pad_x, pad_y = sc(14), sc(10)
    line_h = sc(18)
    inner_w = max(box_dims(h)[0] for h in items)
    panel_w = inner_w + pad_x * 2
    panel_h = pad_y * 2 + sc(16) + max(0, len(items) - 1) * line_h
    x = cx - panel_w // 2
    out = (
        f'  <rect x="{x}" y="{y}" width="{panel_w}" height="{panel_h}" rx="12" '
        f'fill="{C["panel"]}" stroke="{C["border"]}" stroke-width="2" filter="url(#sh)"/>\n'
    )
    out += (
        f'  <text x="{cx}" y="{y + pad_y + sc(14)}" text-anchor="middle" font-family="{FONT}" '
        f'font-size="{sc(11)}" font-weight="700" fill="{C["blue"]}">{esc(items[0])}</text>\n'
    )
    cy = y + pad_y + sc(24)
    for child in items[1:]:
        cy += line_h
        out += (
            f'  <text x="{x + pad_x + sc(6)}" y="{cy}" font-family="{FONT}" '
            f'font-size="{sc(10)}" fill="{C["text"]}">• {esc(child)}</text>\n'
        )
    return out, y + panel_h, panel_w


def render_text_diagram(text: str, title: str = "") -> tuple[str, int, int]:
    lines = [ln.rstrip() for ln in text.strip().splitlines()]
    rows: list[str | list[str]] = []
    for ln in lines:
        s = ln.strip()
        if not s:
            continue
        if is_separator(s):
            if rows and rows[-1] != "GAP":
                rows.append("GAP")
            continue
        if is_decorative_line(ln):
            continue
        if is_arrow_line(s):
            rows.append("ARROW")
            continue
        cols = split_columns(ln)
        if cols and len(cols) >= 2:
            rows.append(cols)
        else:
            rows.append(s)

    while rows and rows[0] == "GAP":
        rows.pop(0)
    while rows and rows[-1] == "GAP":
        rows.pop()
    # Drop GAP between a root label and a column row (CIA triad)
    compact: list[str | list[str]] = []
    for idx, row in enumerate(rows):
        if (
            row == "GAP"
            and compact
            and isinstance(compact[-1], str)
            and compact[-1] not in ("GAP", "ARROW")
            and idx + 1 < len(rows)
            and isinstance(rows[idx + 1], list)
        ):
            continue
        if row == "GAP" and compact and compact[-1] == "GAP":
            continue
        compact.append(row)
    rows = compact

    margin = sc(22)
    gap = sc(10)
    inner: list[str] = []
    y = margin + (sc(28) if title else 0)
    cx = sc(240)
    max_x = cx + sc(140)
    min_x = cx - sc(140)

    if title:
        clean = title if title.lower() not in {"draw", "diagram", "whiteboard diagram"} else "Diagram"
        inner.append(
            f'  <text x="{cx}" y="{margin + sc(12)}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="{sc(12)}" font-weight="700" fill="{C["text"]}">{esc(clean)}</text>\n'
        )
        y = margin + sc(28)

    i = 0
    while i < len(rows):
        row = rows[i]
        if row == "GAP":
            y += gap
            i += 1
            continue
        if row == "ARROW":
            inner.append(render_arrow_down(cx, y, sc(14)))
            y += sc(14)
            i += 1
            continue

        if isinstance(row, list):
            part, y, row_w = render_row(row, cx, y, C["blue_bg"], C["blue_border"])
            inner.append(part)
            min_x = min(min_x, cx - row_w // 2)
            max_x = max(max_x, cx + row_w // 2)
            y += gap
            i += 1
            if i < len(rows) and isinstance(rows[i], list):
                part, y, row_w = render_row(rows[i], cx, y, C["green_bg"], C["green_border"])
                inner.append(part)
                min_x = min(min_x, cx - row_w // 2)
                max_x = max(max_x, cx + row_w // 2)
                y += gap
                i += 1
            continue

        # Group consecutive labels (section lists without arrows)
        run: list[str] = []
        j = i
        while j < len(rows) and isinstance(rows[j], str) and rows[j] not in ("GAP", "ARROW"):
            run.append(rows[j])
            if j + 1 < len(rows) and rows[j + 1] == "ARROW":
                break
            j += 1

        if len(run) >= 3:
            part, y, row_w = render_group_panel(run, cx, y)
            inner.append(part)
            min_x = min(min_x, cx - row_w // 2)
            max_x = max(max_x, cx + row_w // 2)
            y += gap
            i = j + 1 if j < len(rows) and rows[j] == "ARROW" else j
            continue

        label = run[0] if run else str(row)
        w, h = box_dims(label, min_w=104)
        inner.append(render_box(cx - w // 2, y, w, h, label, C["panel"], C["border"]))
        min_x = min(min_x, cx - w // 2)
        max_x = max(max_x, cx + w // 2)
        y += h

        nxt = rows[i + 1] if i + 1 < len(rows) else None

        if nxt == "GAP" and i + 2 < len(rows) and isinstance(rows[i + 2], list):
            inner.append(render_arrow_down(cx, y, sc(12)))
            y += sc(12)
            children = rows[i + 2]
            assert isinstance(children, list)
            part, y, row_w = render_tree_branches(cx, y, w, children, C["panel"], C["border"])
            inner.append(part)
            min_x = min(min_x, cx - row_w // 2)
            max_x = max(max_x, cx + row_w // 2)
            y += gap
            i += 3
            if i < len(rows) and isinstance(rows[i], list):
                part, y, row_w = render_row(rows[i], cx, y, C["green_bg"], C["green_border"])
                inner.append(part)
                min_x = min(min_x, cx - row_w // 2)
                max_x = max(max_x, cx + row_w // 2)
                y += gap
                i += 1
            continue

        if isinstance(nxt, list):
            part, y, row_w = render_tree_branches(cx, y, w, nxt, C["panel"], C["border"])
            inner.append(part)
            min_x = min(min_x, cx - row_w // 2)
            max_x = max(max_x, cx + row_w // 2)
            y += gap
            i += 2
            if i < len(rows) and isinstance(rows[i], list):
                part, y, row_w = render_row(rows[i], cx, y, C["green_bg"], C["green_border"])
                inner.append(part)
                min_x = min(min_x, cx - row_w // 2)
                max_x = max(max_x, cx + row_w // 2)
                y += gap
                i += 1
            continue

        if nxt == "ARROW":
            inner.append(render_arrow_down(cx, y, sc(12)))
            y += sc(12)
            i += 2
            continue

        i += 1

    width = max(sc(260), max_x - min_x + margin * 2)
    height = max(sc(80), y + margin)
    body = "".join(inner)
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'role="img" aria-label="{esc(title or "Diagram")}">\n'
        f"{svg_defs()}"
        f'  <rect width="{width}" height="{height}" fill="{C["bg"]}"/>\n'
        f"{body}</svg>\n"
    )
    svg = add_svg_display_size(svg)
    return svg, width, height


def split_into_sections(content: str) -> list[tuple[str, str]]:
    lines = content.splitlines(keepends=True)
    indices: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        if line.startswith("# Slide Topic:"):
            title = line[2:].strip().replace("Slide Topic:", "").strip()
            indices.append((i, title))
        elif line.startswith("# ") and is_major_topic_header(line[2:].strip()):
            indices.append((i, line[2:].strip()))

    if not indices:
        return [("day1-notes", content)]

    sections: list[tuple[str, str]] = []
    for idx, (start, title) in enumerate(indices):
        end = indices[idx + 1][0] if idx + 1 < len(indices) else len(lines)
        body = "".join(lines[start:end]).strip() + "\n"
        sections.append((title, body))
    return sections


def is_major_topic_header(title: str) -> bool:
    if title.startswith("Slide Topic:"):
        return True
    letters = [c for c in title if c.isalpha()]
    if len(title) >= 18 and letters:
        upper_ratio = sum(c.isupper() for c in letters) / len(letters)
        if upper_ratio >= 0.72:
            return True
    keywords = (
        "MITRE ATT&CK FRAMEWORK",
        "BRUTE FORCE AND CREDENTIAL",
        "PRIVILEGE ESCALATION",
        "WHY LOGS ARE THE FOUNDATION",
        "LINUX LOGGING",
        "COLLECTING SSH EVIDENCE",
        "EVIDENCE AND THE ANALYST",
        "RISK SCORING FUNDAMENTALS",
        "Cloud Security Posture Management (CSPM)",
    )
    return any(title.startswith(k) or k in title for k in keywords)


def extract_headings(md: str) -> list[tuple[int, str, str]]:
    toc: list[tuple[int, str, str]] = []
    seen: dict[str, int] = {}
    for line in md.splitlines():
        m = re.match(r"^(#{1,4})\s+(.+)$", line)
        if not m:
            continue
        level = len(m.group(1))
        title = m.group(2).strip()
        if title.startswith("Slide Topic:"):
            continue
        anchor = heading_anchor(title, seen)
        toc.append((level, title, anchor))
    return toc


def heading_anchor(title: str, seen: dict[str, int]) -> str:
    base = slugify(title)
    seen[base] = seen.get(base, 0) + 1
    return base if seen[base] == 1 else f"{base}-{seen[base]}"


def build_toc(headings: list[tuple[int, str, str]], min_level: int = 2) -> str:
    lines = ["## On this page\n"]
    for level, title, anchor in headings:
        if level < min_level or level > 3:
            continue
        indent = "  " * (level - min_level)
        lines.append(f"{indent}- [{title}](#{anchor})")
    return "\n".join(lines) + "\n\n---\n\n"


def process_diagrams(md: str, section_slug: str, counter: list[int]) -> str:
    pattern = re.compile(r"```text\n(.*?)```", re.DOTALL)
    context_window = 400

    def replacer(match: re.Match[str]) -> str:
        text = match.group(1)
        start = match.start()
        context = md[max(0, start - context_window) : start]
        if not is_diagram_block(text, context):
            return match.group(0)

        counter[0] += 1
        diag_id = f"{section_slug}-{counter[0]:03d}"
        # Derive short title from preceding header
        header_m = re.findall(r"^#{1,3}\s+(.+)$", context, re.MULTILINE)
        diag_title = header_m[-1].strip() if header_m else f"Diagram {counter[0]}"
        if diag_title.lower().startswith("draw"):
            diag_title = "Diagram"

        svg, vb_w, _ = render_text_diagram(text, diag_title)
        svg = add_svg_display_size(svg)
        svg_path = DIAGRAMS / f"{diag_id}.svg"
        svg_path.write_text(svg, encoding="utf-8")

        rel = f"{DIAGRAM_REL}/{diag_id}.svg"
        display_w = int(min(vb_w, DIAGRAM_DISPLAY_WIDTH))
        return format_diagram_embed(diag_title, rel, display_w)

    return pattern.sub(replacer, md)


def demote_headings(md: str, levels: int = 1) -> str:
    out: list[str] = []
    for line in md.splitlines(keepends=True):
        m = re.match(r"^(#{1,6})\s", line)
        if m and len(m.group(1)) + levels <= 6:
            out.append("#" * (len(m.group(1)) + levels) + line[len(m.group(1)) :])
        else:
            out.append(line)
    return "".join(out)


def build_master_toc(section_meta: list[tuple[int, str, str]]) -> str:
    topic_to_block: dict[str, str] = {}
    for block in COURSE_BLOCKS:
        for t in block.get("topics", []):
            topic_to_block[t] = block["name"]

    lines = ["## Table of contents\n"]
    for idx, title, anchor in section_meta:
        block = topic_to_block.get(title, infer_block(title))
        short = title if len(title) <= 60 else title[:57] + "..."
        lines.append(f"{idx}. [{short}](#{anchor}) — *{block}*")
    return "\n".join(lines) + "\n"


def strip_duplicate_section_title(body: str, title: str) -> str:
    """Remove inner ## heading when it repeats the section title."""
    pattern = rf"^## {re.escape(title.strip())}\s*\n+"
    return re.sub(pattern, "", body.strip(), count=1, flags=re.MULTILINE | re.IGNORECASE)


def build_doc_intro(section_meta: list[tuple[int, str, str]]) -> str:
    """No front matter — content starts at the first topic."""
    return ""


def format_section_header(title: str, idx: int) -> str:
    if idx == 1:
        return f"# {title}\n\n"
    return f"\n\n## {title}\n\n"


def compress_markdown(md: str) -> str:
    """Tighten spacing; delegate to shared instructor-notes compactor when available."""
    try:
        import importlib.util
        compact_path = Path(__file__).resolve().parent / "compact_notes.py"
        if compact_path.exists():
            spec = importlib.util.spec_from_file_location("compact_notes", compact_path)
            mod = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(mod)
            return mod.compact_markdown(md)
    except Exception:
        pass
    md = md.replace("\r\n", "\n").replace("\r", "\n")
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n---\n+(?=#{3,6} )", "\n\n", md)
    md = re.sub(r"\n---\n+(?=## (?!.*\{#part-))", "\n\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def reorganize_section_body(body: str) -> str:
    """Remove duplicate slide-topic H1; content follows the part heading."""
    return re.sub(r"^# Slide Topic:\s*.+\n+", "", body, count=1, flags=re.MULTILINE)


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Source not found: {SRC}")

    raw = SRC.read_text(encoding="utf-8")
    DIAGRAMS.mkdir(parents=True, exist_ok=True)

    sections_dir = ROOT / "sections"
    if sections_dir.exists():
        shutil.rmtree(sections_dir)

    for p in DIAGRAMS.glob("*.svg"):
        p.unlink()

    parts = split_into_sections(raw)
    global_counter = [0]
    section_meta: list[tuple[int, str, str]] = []
    content_parts: list[str] = []

    for idx, (title, body) in enumerate(parts, 1):
        slug = slugify(title)
        anchor = f"part-{idx:02d}-{slug}"
        section_meta.append((idx, title, anchor))

        body = reorganize_section_body(body)
        body = process_diagrams(body, slug, global_counter)
        body = demote_headings(body, 1)
        body = strip_duplicate_section_title(body, title)
        content_parts.append(format_section_header(title, idx) + body.strip() + "\n")

    doc = "".join(content_parts)
    doc = compress_markdown(doc)
    OUTPUT.write_text(doc, encoding="utf-8")

    print(f"Built single file: {OUTPUT}")
    print(f"  Topics: {len(section_meta)}, SVG diagrams: {global_counter[0]}")
    print(f"  Diagrams: {DIAGRAMS}")


def infer_block(title: str) -> str:
    upper = title.upper()
    if "MITRE" in upper or "BRUTE FORCE" in upper or "PRIVILEGE" in upper:
        return "SOC & Detection (slides 31–44)"
    if "LOG" in upper or "EVIDENCE" in upper or "RISK SCORING" in upper:
        return "SOC & Detection (slides 31–44)"
    if "AI" in upper and ("LIMITATION" in upper or "WORKFLOW" in upper):
        return "AI in Security (slides 52–65)"
    if "CSPM" in upper or "SECURITY HUB" in upper or "CLOUDTRAIL" in upper or "S3" in upper:
        return "CSPM & AWS Security (slides 73–96)"
    if "MFA" in upper or "IAM ACCESS" in upper:
        return "CSPM & AWS Security (slides 73–96)"
    if "FINDINGS BASELINE" in upper or "SECURITY FINDINGS" in upper:
        return "Lab 1.4 / CSPM (slide 96)"
    return "Day 1 extended topics"


if __name__ == "__main__":
    main()
