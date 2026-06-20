"""Compact instructor notes markdown without removing substantive information."""
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

# Max chars per bullet item to allow inline join
SHORT_ITEM_MAX = 52


def extract_text_blocks(md: str) -> str:
    def repl(match: re.Match[str]) -> str:
        body = match.group(1).strip("\n")
        non_empty = [ln.strip() for ln in body.splitlines() if ln.strip()]
        if not non_empty:
            return ""
        if len(non_empty) == 1:
            line = non_empty[0]
            if len(line) <= 80 and not line.startswith("http"):
                return f" `{line}`"
            return f" {line}"
        if len(non_empty) >= 2 and all(len(x) <= SHORT_ITEM_MAX for x in non_empty):
            return " " + " · ".join(non_empty)
        return "\n" + "\n".join(f"- {ln}" for ln in non_empty)

    return re.sub(r"```text\n(.*?)```", repl, md, flags=re.DOTALL)


def compact_diagrams(md: str) -> str:
    """Replace inline SVG images with compact links (same path + alt text)."""
    md = re.sub(r"^## Whiteboard Diagram\s*\n+", "", md, flags=re.MULTILINE)
    md = re.sub(r"^## Visual Diagram\s*\n+", "", md, flags=re.MULTILINE)
    md = re.sub(r"\nDraw:\n", "\n", md)

    def repl(match: re.Match[str]) -> str:
        alt = match.group(1).strip() or "Diagram"
        path = match.group(2)
        return f"→ [{alt}]({path})"

    return re.sub(r"!\[([^\]]*)\]\(([^)]+\.svg)\)", repl, md)


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
        "diagrams linked as → [title](path.svg) — click to open",
    )
    md = md.replace(
        "Diagrams appear as SVG images inline.",
        "Diagrams appear as compact links (SVG files open on click).",
    )
    md = re.sub(r"(\|[^\n]+\|)\n\n(?=\|)", r"\1\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n\n"


def compact_h4_sections(md: str) -> str:
    # Empty h4 title-only headers
    md = re.sub(r"^#### ([^\n]+)\n+(?=#### )", r"**\1** · ", md, flags=re.MULTILINE)
    md = re.sub(r"^#### ([^\n]+)\n+(?=## )", r"**\1**\n", md, flags=re.MULTILINE)

    def repl(match: re.Match[str]) -> str:
        label = match.group(1).strip()
        body = match.group(2).strip()
        if not body:
            return f"**{label}**"
        body_lines = [
            ln.strip()
            for ln in body.splitlines()
            if ln.strip() and not re.match(r"^#{1,4} ", ln)
        ]
        if not body_lines:
            return f"**{label}**"
        if len(body_lines) == 1 and not body_lines[0].startswith(("*", "-", "→")):
            if body_lines[0].endswith(":") and len(body_lines[0]) < 24:
                return f"**{label}**\n{body_lines[0]}\n"
            return f"**{label}:** {body_lines[0]}"
        if label.startswith("Q:"):
            return f"**{label}** {body_lines[0]}"
        if all(len(x) <= SHORT_ITEM_MAX for x in body_lines):
            return f"**{label}:** " + " · ".join(body_lines)
        return f"**{label}**\n" + "\n".join(body_lines)

    return re.sub(
        r"^#### (.+?)\n+((?:(?!^#{1,4} ).+?(?:\n|$))+)",
        repl,
        md,
        flags=re.MULTILINE,
    )


def compact_qa_blocks(md: str) -> str:
    md = re.sub(r"\*\*Q:\*\*\s*\n+", "**Q:** ", md)
    md = re.sub(r"\*\*Answer:\*\*\s*\n+", "**Answer:** ", md)
    md = re.sub(r"\*\*Student Question\*\*\s*\n+", "**Student Question** ", md)
    return md


def _join_bullet_items(items: list[str]) -> str:
    return " · ".join(items)


def compact_short_bullet_blocks(md: str) -> str:
    """Merge consecutive short * / - bullets into one line."""
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    bullet_re = re.compile(r"^([\*\-]|\d+\.)\s+(.+)$")

    while i < len(lines):
        m = bullet_re.match(lines[i].strip())
        if not m:
            out.append(lines[i])
            i += 1
            continue

        items: list[str] = []
        j = i
        while j < len(lines):
            bm = bullet_re.match(lines[j].strip())
            if not bm:
                break
            items.append(bm.group(2).strip())
            j += 1

        if len(items) >= 2 and all(len(it) <= SHORT_ITEM_MAX for it in items):
            joined = _join_bullet_items(items)
            prev = out[-1].strip() if out else ""
            if prev.endswith(":") and not prev.startswith("#"):
                out[-1] = out[-1].rstrip() + " " + joined
            elif re.match(r"^\*\*.+\*\*:?$", prev) and not prev.startswith("#"):
                out[-1] = out[-1].rstrip().rstrip(":") + ": " + joined
            else:
                out.append(joined)
            i = j
            continue

        for k in range(i, j):
            out.append(lines[k])
        i = j

    return "\n".join(out)


def compact_blockquotes(md: str) -> str:
    """Remove blank lines between blockquote lines; keep labels on separate lines."""
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        if not lines[i].startswith(">"):
            out.append(lines[i])
            i += 1
            continue
        while i < len(lines) and lines[i].startswith(">"):
            out.append(lines[i])
            i += 1
    return "\n".join(out)


def compact_part_headers(md: str) -> str:
    return re.sub(
        r"^\*Part (\d+) of (\d+) · (.+)\*$",
        r"*§\1/\2 · \3*",
        md,
        flags=re.MULTILINE,
    )


def remove_redundant_rules(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    for i, line in enumerate(lines):
        if line.strip() != "---":
            out.append(line)
            continue
        nxt = next((lines[j] for j in range(i + 1, min(i + 4, len(lines))) if lines[j].strip()), "")
        prev = out[-1].strip() if out else ""
        if nxt.startswith("## ") and "{#part-" in nxt:
            out.append(line)
        elif "Day" in prev and "content" in prev.lower():
            out.append(line)
    return "\n".join(out)


def remove_label_gaps(md: str) -> str:
    """Join label lines with following inline content (not blockquotes)."""
    return re.sub(
        r"^([A-Za-z][^\n:]{0,60}:)\n+(?=[`\*\-0-9]|→ )",
        r"\1 ",
        md,
        flags=re.MULTILINE,
    )


def ultra_collapse_blanks(md: str) -> str:
    """Single newlines; blank line only before part anchor headers."""
    lines = [ln.rstrip() for ln in md.splitlines()]
    out: list[str] = []
    for line in lines:
        if not line.strip():
            continue
        if line.startswith("## ") and "{#part-" in line and out and out[-1].strip():
            out.append("")
        out.append(line)
    return "\n".join(out)


def fix_header_collisions(md: str) -> str:
    """Prevent 'Known as:## Title' and similar merges."""
    md = re.sub(
        r"This slide introduces:\s*\n*#### Confidentiality\s*\n*\*\*Integrity\*\*\s*\*\*Availability:\*\* Known as:\s*\n*## CIA Triad",
        "This slide introduces: **Confidentiality** · **Integrity** · **Availability**\nKnown as:\n\n## CIA Triad",
        md,
        flags=re.IGNORECASE,
    )
    md = re.sub(
        r"This slide introduces: \*\*Confidentiality:\*\* \*\*Integrity\*\* · \*\*Availability:\*\* Known as:",
        "This slide introduces: **Confidentiality** · **Integrity** · **Availability**\nKnown as:",
        md,
    )
    md = re.sub(r"([.:!?])(## )", r"\1\n\n\2", md)
    return md


def collapse_blank_lines(md: str) -> str:
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def compact_markdown(md: str) -> str:
    md = md.replace("\r\n", "\n").replace("\r", "\n")
    preamble, body = split_preamble_body(md)
    body = extract_text_blocks(body)
    body = compact_diagrams(body)
    body = remove_filler_lines(body)
    body = compact_h4_sections(body)
    body = compact_qa_blocks(body)
    body = compact_short_bullet_blocks(body)
    body = compact_blockquotes(body)
    body = compact_part_headers(body)
    body = remove_label_gaps(body)
    body = remove_redundant_rules(body)
    body = ultra_collapse_blanks(body)
    body = fix_header_collisions(body)
    body = collapse_blank_lines(body)
    preamble = compact_preamble(preamble)
    return (preamble + body).strip() + "\n"


def normalize_for_compare(text: str) -> str:
    t = re.sub(r"```text\n(.*?)```", r"\1", text, flags=re.DOTALL)
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
        root / "day1" / "day1_instructor_notes.md",
        root / "day2" / "day2_instructor_notes.md",
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
