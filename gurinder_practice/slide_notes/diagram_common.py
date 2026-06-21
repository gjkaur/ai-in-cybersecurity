"""Shared diagram detection and text-block parsing for study notes."""
from __future__ import annotations

import re

BOX_DRAWING = set("┌┐└┘│─┼┴┬├┤▼▲→←↓↑▶◀")


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


def has_box_drawing(text: str) -> bool:
    return any(c in BOX_DRAWING for c in text)


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


def parse_diagram_rows(text: str) -> list[str | list[str]]:
    """Parse a ```text diagram block into rows (same logic as legacy SVG builder)."""
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
    return compact


def split_into_sections(content: str) -> list[tuple[str, str]]:
    lines = content.splitlines(keepends=True)
    if any(line.startswith("# Slide Topic:") for line in lines):
        indices: list[tuple[int, str]] = []
        for i, line in enumerate(lines):
            if line.startswith("# Slide Topic:"):
                title = line[2:].strip().replace("Slide Topic:", "").strip()
                indices.append((i, title))
            elif line.startswith("# ") and is_major_topic_header(line[2:].strip()):
                indices.append((i, line[2:].strip()))
    else:
        indices = [(i, line[2:].strip()) for i, line in enumerate(lines) if line.startswith("# ")]

    if not indices:
        return [("notes", content)]

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
