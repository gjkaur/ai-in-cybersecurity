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


def extract_text_blocks(md: str) -> str:
    """Convert ```text blocks to bullet lists (readable, not inline joins)."""

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
        return f"\n→ [{alt}]({path})\n"

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


def compact_qa_blocks(md: str) -> str:
    md = re.sub(r"\*\*Q:\*\*\s*\n+", "**Q:** ", md)
    md = re.sub(r"\*\*Answer:\*\*\s*\n+", "\n\n**Answer:** ", md)
    # Split inline Q/A: **Q: ...?:** Answer
    md = re.sub(
        r"^\*\*Q: (.+?)\?\*\*: (.+)$",
        r"**Q:** \1?\n\n**Answer:** \2",
        md,
        flags=re.MULTILINE,
    )
    # Blank line between Student Question label and Q
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

        # Collect a blockquote run (skip blank lines and lone '>' between quote lines)
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
    # Sentence glued to next heading: "...compromise.## Linux Permissions"
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
            return True
        if line.startswith(">"):
            return True
        if line.startswith("→ ["):
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


def compact_markdown(md: str) -> str:
    md = md.replace("\r\n", "\n").replace("\r", "\n")
    preamble, body = split_preamble_body(md)
    body = extract_text_blocks(body)
    body = compact_diagrams(body)
    body = remove_filler_lines(body)
    body = fix_content_corruption(body)
    body = compact_qa_blocks(body)
    body = compact_blockquotes(body)
    body = compact_part_headers(body)
    body = preserve_section_spacing(body)
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
