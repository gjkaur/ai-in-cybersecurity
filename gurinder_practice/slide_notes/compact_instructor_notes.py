"""Compact instructor notes markdown without removing information."""
from __future__ import annotations

import re
import sys
from pathlib import Path


def extract_text_blocks(md: str) -> str:
    """Convert ```text fences to compact inline or list form (content preserved)."""

    def repl(match: re.Match[str]) -> str:
        body = match.group(1).strip("\n")
        lines = [ln.rstrip() for ln in body.splitlines()]
        while lines and not lines[0].strip():
            lines.pop(0)
        while lines and not lines[-1].strip():
            lines.pop()
        non_empty = [ln.strip() for ln in lines if ln.strip()]
        if not non_empty:
            return ""

        if len(non_empty) == 1:
            line = non_empty[0]
            if len(line) <= 72 and not line.startswith("http"):
                return f"\n`{line}`\n"
            return f"\n{line}\n"

        # Multi-line: use bullet list (each line preserved)
        return "\n" + "\n".join(f"- {ln}" for ln in non_empty) + "\n"

    return re.sub(r"```text\n(.*?)```", repl, md, flags=re.DOTALL)


def compact_h4_sections(md: str) -> str:
    """#### Label + body -> **Label:** body (single-line body) or tighter block."""

    def repl(match: re.Match[str]) -> str:
        label = match.group(1).strip()
        body = match.group(2).strip()
        if not body:
            return f"**{label}**"
        body_lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
        if len(body_lines) == 1 and not body_lines[0].startswith("*"):
            return f"**{label}:** {body_lines[0]}"
        if label.startswith("Q:"):
            return f"**{label}** {body_lines[0] if body_lines else ''}" + (
                ("\n" + "\n".join(body_lines[1:])) if len(body_lines) > 1 else ""
            )
        # Multi-paragraph: keep label bold, tighten spacing
        return f"**{label}**\n" + "\n".join(body_lines)

    # #### header followed by content until next header/block
    return re.sub(
        r"^#### (.+?)\n\n((?:(?!^#{1,4} ).+(?:\n|$))+)",
        repl,
        md,
        flags=re.MULTILINE,
    )


def compact_qa_blocks(md: str) -> str:
    """Tighten **Q:** / **Answer:** pairs."""

    md = re.sub(r"\*\*Q:\*\*\s*\n\n", "**Q:** ", md)
    md = re.sub(r"\*\*Answer:\*\*\s*\n\n", "**Answer:** ", md)
    return md


def compact_blockquotes(md: str) -> str:
    """Remove blank lines between consecutive blockquote lines."""
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith(">"):
            block: list[str] = []
            while i < len(lines) and (lines[i].startswith(">") or lines[i].strip() == ""):
                if lines[i].startswith(">"):
                    block.append(lines[i])
                i += 1
            out.extend(block)
            continue
        out.append(line)
        i += 1
    return "\n".join(out)


def remove_redundant_rules(md: str) -> str:
    """Drop --- except before ## part sections and after intro TOC."""
    lines = md.splitlines()
    out: list[str] = []
    for i, line in enumerate(lines):
        if line.strip() != "---":
            out.append(line)
            continue
        # peek ahead for part heading
        nxt = next((lines[j] for j in range(i + 1, min(i + 4, len(lines))) if lines[j].strip()), "")
        prev = out[-1].strip() if out else ""
        if nxt.startswith("## ") and "{#part-" in nxt:
            out.append(line)
        elif prev.startswith("# Day") and "content" in prev.lower():
            out.append(line)
        # skip other ---
    return "\n".join(out)


def collapse_blank_lines(md: str) -> str:
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    # No blank line between list items
    md = re.sub(r"(\n[*-] .+)\n\n(?=[*-] )", r"\1\n", md)
    # No blank line between numbered list items
    md = re.sub(r"(\n\d+\. .+)\n\n(?=\d+\. )", r"\1\n", md)
    # Single blank before headers (not double)
    md = re.sub(r"\n{2,}(#{1,6} )", r"\n\n\1", md)
    return md.strip() + "\n"


def remove_label_gaps(md: str) -> str:
    """Remove blank line after lines ending with colon when followed by content."""
    labels = (
        r"Tell students:",
        r"Ask the class:",
        r"Then ask:",
        r"Simple version:",
        r"Physical World:",
        r"Digital World:",
        r"Without cybersecurity:",
        r"Cybersecurity protects:",
        r"Examples:",
        r"Problem:",
        r"Original:",
        r"Encrypted:",
        r"Who should see it\?",
        r"Organizations depend on:",
        r"from:",
        r"Problem:",
        r"Traditional Security:",
        r"AI-Assisted Security:",
        r"Important teaching point:",
        r"A typical enterprise may generate:",
        r"AI helps by:",
        r"No\.",
        r"It includes:",
        r"Everyone needs cybersecurity:",
    )
    for label in labels:
        md = re.sub(rf"({label})\n\n", r"\1\n", md)
    return md


def fix_blockquote_transitions(md: str) -> str:
    """Ensure newline before non-blockquote line after blockquote."""
    return re.sub(r"(\n(?:> .+\n)+)(?=[A-Za-z*#])", r"\1\n", md)


def compact_markdown(md: str) -> str:
    md = md.replace("\r\n", "\n").replace("\r", "\n")
    md = extract_text_blocks(md)
    md = compact_h4_sections(md)
    md = compact_qa_blocks(md)
    md = compact_blockquotes(md)
    md = remove_label_gaps(md)
    md = fix_blockquote_transitions(md)
    md = remove_redundant_rules(md)
    md = collapse_blank_lines(md)
    return md


def token_set(text: str) -> set[str]:
    t = normalize_for_compare(text)
    return set(re.findall(r"[a-z0-9]+", t))


def content_preserved(original: str, compacted: str) -> bool:
    orig = token_set(original)
    comp = token_set(compacted)
    missing = orig - comp
    # Allow minor tokenizer diffs from punctuation-only tokens
    significant = {w for w in missing if len(w) > 2}
    return len(significant) == 0


def word_count(text: str) -> int:
    return len(re.findall(r"\S+", text))


def normalize_for_compare(text: str) -> str:
    """Strip formatting to verify textual content preserved."""
    t = re.sub(r"```text\n(.*?)```", r"\1", text, flags=re.DOTALL)
    t = re.sub(r"```\w*\n(.*?)```", r"\1", t, flags=re.DOTALL)
    t = re.sub(r"!\[[^\]]*\]\([^)]+\)", " ", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"[#*`>|_\-]", " ", t)
    t = re.sub(r"\s+", " ", t).strip().lower()
    return t


def compact_file(path: Path) -> tuple[int, int, bool]:
    original = path.read_text(encoding="utf-8")
    compacted = compact_markdown(original)
    path.write_text(compacted, encoding="utf-8")
    ok = content_preserved(original, compacted)
    return len(original.splitlines()), len(compacted.splitlines()), ok


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
        before_lines, after_lines, content_ok = compact_file(path)
        pct = 100 * (1 - after_lines / before_lines) if before_lines else 0
        status = "OK" if content_ok else "CHECK"
        print(f"{path.name}: {before_lines} -> {after_lines} lines ({pct:.1f}% reduction) [{status}]")


if __name__ == "__main__":
    main()
