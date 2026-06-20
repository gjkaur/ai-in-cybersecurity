"""Compact study notes markdown without removing substantive information."""
from __future__ import annotations

import re
import sys
from pathlib import Path

# Lines removed as instructor filler (not substantive content)
FILLER_LINE_PATTERNS = (
    r"^Let's expand\.?$",
    r"^Same concept\.?$",
    r"^Draw:?$",
    r"^The slide mentions:?$",
    r"^Little technical knowledge\.?$",
    r"^Students often confuse these\.?$",
    r"^Since this course is AI in Cybersecurity, connect immediately\.?$",
)

TEXT_FENCE_RE = re.compile(r"```text(?: id=\"[^\"]+\")?\n(.*?)```", re.DOTALL)
BULLET_RE = re.compile(r"^-\s+(.+)$")
TABLE_ROW_RE = re.compile(r"^\|.+\|$")
DIAGRAM_CHARS = set("┌┐└┘│─┼┴┬├┤▼▲→←↓↑▶◀")
CONNECTOR_ONLY_RE = re.compile(r"^[│▼▲→←↓↑▶◀|\s]+$")


def has_diagram_markers(text: str) -> bool:
    return any(c in DIAGRAM_CHARS for c in text) or "──" in text


def is_connector_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    return bool(CONNECTOR_ONLY_RE.match(s)) or s in {"↓", "→", "│", "▼", "▲"}


def is_markdown_table_lines(lines: list[str]) -> bool:
    pipe_rows = [ln for ln in lines if "|" in ln and len(ln.split("|")) >= 3]
    return len(pipe_rows) >= 2 and len(pipe_rows) >= len(lines) // 2


def format_table_lines(lines: list[str]) -> str:
    rows = [ln.strip() for ln in lines if ln.strip()]
    return "\n".join(rows)


def collapse_diagram_blanks(body: str) -> str:
    """Keep diagram shape; collapse 3+ blank lines to one inside code blocks."""
    lines = body.splitlines()
    out: list[str] = []
    blank_run = 0
    for line in lines:
        if not line.strip():
            blank_run += 1
            if blank_run <= 1:
                out.append("")
            continue
        blank_run = 0
        out.append(line.rstrip())
    while out and not out[-1].strip():
        out.pop()
    while out and not out[0].strip():
        out.pop(0)
    return "\n".join(out)


def format_text_block_body(body: str) -> str:
    body = body.strip("\n")
    lines = body.splitlines()
    stripped = [ln.strip() for ln in lines if ln.strip()]

    if not stripped:
        return ""

    if has_diagram_markers(body) or sum(1 for ln in lines if is_connector_line(ln)) >= 2:
        return f"\n```text\n{collapse_diagram_blanks(body)}\n```\n"

    if is_markdown_table_lines(stripped):
        return "\n" + format_table_lines(stripped) + "\n"

    if len(stripped) == 1:
        line = stripped[0]
        if len(line) <= 80 and not line.startswith("http"):
            return f" `{line}`"
        return f" {line}"

    return "\n" + "\n".join(f"- {ln}" for ln in stripped)


def extract_text_blocks(md: str) -> str:
    """Format ```text blocks as bullets, tables, or monospace ASCII diagrams."""

    def repl(match: re.Match[str]) -> str:
        return format_text_block_body(match.group(1))

    return TEXT_FENCE_RE.sub(repl, md)


def normalize_text_fences(md: str) -> str:
    return re.sub(r"```text id=\"[^\"]+\"", "```text", md)


def bullet_run_is_diagram(items: list[str]) -> bool:
    if not items:
        return False
    if any(has_diagram_markers(it) or is_connector_line(it) for it in items):
        return True
    connectors = sum(1 for it in items if is_connector_line(it))
    return connectors >= 2 and len(items) >= 3


def fix_diagram_bullets(md: str) -> str:
    """Rejoin bullet lists that were ASCII diagrams into fenced code blocks."""
    lines = md.splitlines()
    out: list[str] = []
    i = 0

    while i < len(lines):
        m = BULLET_RE.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue

        items: list[str] = []
        j = i
        while j < len(lines):
            bm = BULLET_RE.match(lines[j])
            if not bm:
                break
            items.append(bm.group(1))
            j += 1

        if bullet_run_is_diagram(items):
            while items and not items[-1].strip():
                items.pop()
            while items and not items[0].strip():
                items.pop(0)
            out.append("```text")
            out.extend(items)
            out.append("```")
        else:
            out.extend(lines[i:j])
        i = j

    return "\n".join(out)


def fix_markdown_tables(md: str) -> str:
    """Remove blank lines between consecutive markdown table rows."""
    while True:
        updated = re.sub(r"(\|.+\|)\n+\n(?=\|)", r"\1\n", md)
        if updated == md:
            break
        md = updated
    return md


def compact_diagrams(md: str) -> str:
    """Replace inline SVG images with visible markdown image embeds."""
    md = re.sub(r"^## Whiteboard Diagram\s*\n+", "", md, flags=re.MULTILINE)
    md = re.sub(r"^## Visual Diagram\s*\n+", "", md, flags=re.MULTILINE)
    md = re.sub(r"\nDraw:\n", "\n", md)

    def repl(match: re.Match[str]) -> str:
        alt = match.group(1).strip() or "Diagram"
        path = match.group(2)
        return f"\n![{alt}]({path})\n"

    md = re.sub(r"!\[([^\]]*)\]\(([^)]+\.svg)\)", repl, md)
    md = re.sub(r"→ \[([^\]]*)\]\(([^)]+\.svg)\)", repl, md)
    return md


def remove_filler_lines(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    for line in lines:
        stripped = line.strip()
        if any(re.match(p, stripped, re.I) for p in FILLER_LINE_PATTERNS):
            continue
        out.append(line)
    return "\n".join(out)


def split_preamble_body(md: str) -> tuple[str, str]:
    m = re.search(r"^(# Day \d+ content\s*)$", md, re.MULTILINE)
    if not m:
        return "", md
    return md[: m.start()], md[m.start() :]


def compact_preamble(md: str) -> str:
    if not md.strip():
        return md
    md = md.replace(
        "diagrams are rendered as SVG inline",
        "diagrams display inline as SVG images in `diagrams/`",
    )
    md = md.replace(
        "diagrams display as SVG images (linked files in `diagrams/`)",
        "diagrams display inline as SVG images in `diagrams/`",
    )
    md = md.replace(
        "Diagrams appear as SVG images inline.",
        "Diagrams render inline as `![title](diagrams/*.svg)` images.",
    )
    md = md.replace(
        "Diagrams appear as compact links (SVG files open on click).",
        "Diagrams render inline as `![title](diagrams/*.svg)` images.",
    )
    md = fix_markdown_tables(md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n\n"


def compact_qa_blocks(md: str) -> str:
    md = re.sub(r"\*\*Q:\*\*\s*\n+", "**Q:** ", md)
    md = re.sub(r"\*\*Answer:\*\*\s*\n+", "\n\n**Answer:** ", md)
    md = re.sub(
        r"^\*\*Q: (.+?)\?\*\*: (.+)$",
        r"**Q:** \1?\n\n**Answer:** \2",
        md,
        flags=re.MULTILINE,
    )
    md = re.sub(
        r"(^## Student Questions?\s*\n)\*\*Q:",
        r"\1\n**Q:",
        md,
        flags=re.MULTILINE,
    )
    md = re.sub(
        r"(^\*\*Student Question\*\*\s*\n)\*\*Q:",
        r"\1\n**Q:",
        md,
        flags=re.MULTILINE,
    )
    return md


def compact_blockquotes(md: str) -> str:
    """Clean blockquotes: drop blank gaps and empty '>' separator lines."""
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.startswith(">"):
            out.append(line)
            i += 1
            continue

        quote_lines: list[str] = []
        while i < len(lines):
            cur = lines[i]
            if cur.startswith(">"):
                content = cur[1:].strip()
                if content:
                    quote_lines.append(f"> {content}")
                i += 1
                continue
            if not cur.strip():
                i += 1
                continue
            break

        out.extend(quote_lines)

    return "\n".join(out)


def compact_part_headers(md: str) -> str:
    return re.sub(
        r"^\*Part (\d+) of (\d+) · (.+)\*$",
        r"*§\1/\2 · \3*",
        md,
        flags=re.MULTILINE,
    )


def fix_content_corruption(md: str) -> str:
    """Fix known merge/corruption artifacts from earlier compaction passes."""
    md = re.sub(
        r"This slide introduces:\s*\n+\s*#### Confidentiality\s*\n+\s*\*\*Integrity\*\*\s*\n*\*\*Availability:\*\* Known as:## CIA Triad",
        "This slide introduces:\n\n- **Confidentiality**\n- **Integrity**\n- **Availability**\n\nKnown as the **CIA Triad**.",
        md,
        flags=re.IGNORECASE,
    )
    md = re.sub(
        r"\*\*Availability:\*\* Known as:## CIA Triad",
        "**Availability**\n\nKnown as the **CIA Triad**.",
        md,
    )
    md = re.sub(r"([.!?])(## )", r"\1\n\n\2", md)
    return md


def preserve_section_spacing(md: str) -> str:
    """Keep one blank line before major breaks; never collapse to a wall of text."""
    lines = [ln.rstrip() for ln in md.splitlines()]
    out: list[str] = []

    def needs_blank_before(line: str) -> bool:
        s = line.strip()
        if not s:
            return False
        if s == "---":
            return True
        if line.startswith("## ") and "{#part-" in line:
            return True
        if line.startswith("## ") or line.startswith("### "):
            return True
        if line.startswith("|"):
            if out and out[-1].strip().startswith("|"):
                return False
            return True
        if line.startswith(">"):
            return True
        if line.startswith("→ ["):
            return True
        if line.startswith("!["):
            return True
        if line.startswith("```") and line.strip() != "```":
            return True
        return False

    for line in lines:
        if not line.strip():
            if out and out[-1].strip():
                out.append("")
            continue
        if out and out[-1].strip() and needs_blank_before(line):
            out.append("")
        out.append(line)

    return "\n".join(out)


def collapse_blank_lines(md: str) -> str:
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def trim_study_notes(md: str) -> str:
    """Drop TOC, footers, part labels, and excess dividers."""
    for pat in (
        r"## What is Cybersecurity\?",
        r"# What is Cybersecurity\?",
        r"## From Detection to Investigation",
        r"# From Detection to Investigation",
    ):
        m = re.search("^" + pat, md, re.MULTILINE | re.IGNORECASE)
        if m:
            md = md[m.start() :]
            break
    else:
        md = re.sub(
            r"^# Day \d+ — Refined Instructor Notes.*?(?=^## )",
            "",
            md,
            count=1,
            flags=re.DOTALL | re.MULTILINE,
        )
        md = re.sub(r"^# Day \d+ content\s*\n+", "", md, flags=re.MULTILINE)

    md = re.sub(r"^\*§\d+/\d+ · .+\*\s*\n", "", md, flags=re.MULTILINE)
    md = re.sub(r"^\*Part \d+ of \d+ · .+\*\s*\n", "", md, flags=re.MULTILINE)
    md = re.sub(r"\s*\{#[^}]+\}", "", md)
    md = re.sub(
        r"\n---\n+\*Generated from[^\n]+do not edit this file by hand\.\*\s*",
        "\n",
        md,
        flags=re.DOTALL,
    )
    md = re.sub(r"^## Table of contents.*?^(?=## |\Z)", "", md, flags=re.DOTALL | re.MULTILINE)
    md = re.sub(r"^## Course flow.*?^(?=## |\Z)", "", md, flags=re.DOTALL | re.MULTILINE)
    md = re.sub(r"^## Notes\s*\n(?:- .+\n?)+\n+", "", md, flags=re.MULTILINE)
    md = re.sub(r"\n---\n+(?=#### )", "\n\n", md)
    md = re.sub(r"\n---\n+(?=## )", "\n\n", md)
    md = re.sub(
        r"^(# What is Cybersecurity\?\n\n)"
        r"This is the foundation slide for the entire course\.[^\n]+\n\n",
        r"\1",
        md,
        count=1,
    )
    return md


def compact_markdown(md: str) -> str:
    md = md.replace("\r\n", "\n").replace("\r", "\n")
    preamble, body = split_preamble_body(md)
    body = normalize_text_fences(body)
    body = fix_diagram_bullets(body)
    body = extract_text_blocks(body)
    body = compact_diagrams(body)
    body = remove_filler_lines(body)
    body = fix_content_corruption(body)
    body = compact_qa_blocks(body)
    body = compact_blockquotes(body)
    body = compact_part_headers(body)
    body = preserve_section_spacing(body)
    body = fix_markdown_tables(body)
    body = collapse_blank_lines(body)
    body = fix_markdown_tables(body)
    body = trim_study_notes(body)
    preamble = compact_preamble(preamble)
    combined = (preamble + body).strip() + "\n"
    combined = trim_study_notes(combined)
    refine_path = Path(__file__).resolve().parent / "refine_self_study_notes.py"
    if refine_path.exists():
        try:
            import importlib.util

            spec = importlib.util.spec_from_file_location("refine_self_study", refine_path)
            mod = importlib.util.module_from_spec(spec)
            assert spec.loader is not None
            spec.loader.exec_module(mod)
            return mod.refine_to_self_study(combined)
        except Exception:
            pass
    return combined


def normalize_for_compare(text: str) -> str:
    t = TEXT_FENCE_RE.sub(r"\1", text)
    t = re.sub(r"```\w*\n(.*?)```", r"\1", t, flags=re.DOTALL)
    t = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", t)
    t = re.sub(r"→ \[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"[#*`>|_\-→§]", " ", t)
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t


def token_set(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]{3,}", normalize_for_compare(text)))


def content_preserved(original: str, compacted: str) -> bool:
    orig = token_set(remove_filler_lines(original))
    comp = token_set(compacted)
    missing = orig - comp
    return len(missing) <= 3


def compact_file(path: Path) -> tuple[int, int, bool, int]:
    original = path.read_text(encoding="utf-8")
    compacted = compact_markdown(original)
    path.write_text(compacted, encoding="utf-8")
    ok = content_preserved(original, compacted)
    missing = len(token_set(remove_filler_lines(original)) - token_set(compacted))
    return len(original.splitlines()), len(compacted.splitlines()), ok, missing


def main() -> None:
    root = Path(__file__).resolve().parent
    targets = [
        root / "day1_study_notes.md",
        root / "day2_study_notes.md",
    ]
    if len(sys.argv) > 1:
        targets = [Path(p) for p in sys.argv[1:]]

    for path in targets:
        if not path.exists():
            print(f"Skip (missing): {path}")
            continue
        before, after, ok, missing = compact_file(path)
        pct = 100 * (1 - after / before) if before else 0
        status = "OK" if ok else f"CHECK ({missing} tokens)"
        print(f"{path.name}: {before} -> {after} lines ({pct:.1f}% reduction) [{status}]")


if __name__ == "__main__":
    main()
