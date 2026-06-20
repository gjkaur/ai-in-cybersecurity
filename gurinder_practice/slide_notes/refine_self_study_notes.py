"""Convert instructor slide notes to self-study tone (second person, no classroom prompts)."""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path


def _compact_module():
    path = Path(__file__).resolve().parent / "compact_notes.py"
    spec = importlib.util.spec_from_file_location("_compact_notes", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


def collapse_blank_lines(md: str) -> str:
    return _compact_module().collapse_blank_lines(md)


def trim_study_notes(md: str) -> str:
    return _compact_module().trim_study_notes(md)

# Headings: instructor framing → self-study framing
HEADING_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    (r"^## Instructor Opening \(How to Start Teaching\)\s*$", "## Getting Started"),
    (r"^## Instructor Opening\s*$", "## Getting Started"),
    (r"^### Instructor Opening\s*$", "### Getting Started"),
    (r"^## Important Instructor Discussion\s*$", "## Discussion Points"),
    (r"^## Important Instructor Statement\s*$", "## Key Point"),
    (r"^## Instructor Insight\s*$", "## Insight"),
    (r"^## Instructor Key Takeaway\s*$", "## Key Takeaway"),
    (r"^## Key Instructor Takeaway\s*$", "## Key Takeaway"),
    (r"^## Key Takeaway for Students\s*$", "## Key Takeaway"),
    (r"^## Instructor Story\s*$", "## Real-World Example"),
    (r"^## One-Sentence Summary for Teaching\s*$", "## One-Sentence Summary"),
    (r"^## Likely Student Questions\s*$", "## Common Questions"),
    (r"^## Student Questions\s*$", "## Common Questions"),
    (r"^## Industry Statistics You Can Mention\s*$", "## Industry Statistics"),
    (r"^## MITRE ATT&CK FRAMEWORK – Instructor Notes\s*$", "## MITRE ATT&CK Framework"),
    (r"^### What Participants Will Learn\s*$", "### What You Will Learn"),
    (r"^#### Questions Every Analyst Should Ask\s*$", "#### Questions to Ask During Investigation"),
    (r"^#### Instructor Talking Point\s*$", "#### Key Point"),
    (r"^### Instructor Talking Point\s*$", "### Key Point"),
    (r"^## Instructor Talking Point\s*$", "## Key Point"),
    (r"^## Instructor Discussion Question\s*$", "## Discussion Question"),
    (r"^## Instructor Demonstration Talking Point\s*$", "## Walkthrough Notes"),
    (r"^## Instructor Demonstration\s*$", "## Walkthrough"),
    (r"^## Important Note for Students\s*$", "## Important Note"),
    (r"^## Useful Commands for Students\s*$", "## Useful Commands"),
)

# Lines to drop entirely (instructional meta, not substantive content)
DROP_LINE_PATTERNS: tuple[str, ...] = (
    r"^Tell students:\s*$",
    r"^Tell them:\s*$",
    r"^Then ask:\s*$",
    r"^As an instructor, tell students:\s*$",
    r"^As an instructor, don't just explain AWS\. Explain\s*$",
    r"^As an instructor,\s*$",
    r"^Let's expand\.?$",
    r"^Same concept\.?$",
    r"^Draw:\s*$",
    r"^The slide mentions:\s*$",
    r"^Little technical knowledge\.?$",
    r"^Students often confuse these\.?$",
    r"^Since this course is AI in Cybersecurity, connect immediately\.?$",
    r"^At the end of this section, students should understand:\s*$",
)

# Whole-line rewrites
LINE_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    (r"^Ask the class:\s*$", "**Reflect:**"),
    (r"^Ask yourself:\s*$", "**Reflect:**"),
    (r"^Ask:\s*$", "**Reflect:**"),
    (r"^At the end of this slide, say:\s*$", "**Summary:**"),
    (r"^Students usually answer:\s*$", "Typical answers include:"),
    (r"^Students usually say (.+)\.\s*$", r"Common answer: \1."),
    (r"^Students will understand:\s*$", "You should understand:"),
    (r"^Students will often see:\s*$", "You will often see:"),
    (r"^Students usually struggle here\.\s*$", "This topic is often challenging."),
    (r"^Students will immediately understand (.+)\.\s*$", r"This makes it clear: \1."),
)

# Phrase-level rewrites (order matters — longer phrases first)
PHRASE_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    (r"\bAsk the class:\s*", "**Reflect:** "),
    (r"\bAs an instructor, tell students:\s*", ""),
    (r"\bAs an instructor,\s*", ""),
    (r"\bThis slide introduces\b", "This section covers"),
    (r"\bThis slide explains\b", "This section explains"),
    (r"\bThis slide demonstrates\b", "This section demonstrates"),
    (r"\bThis slide teaches\b", "This section covers"),
    (r"This slide answers:", "This section answers:"),
    (r"This slide focuses on:", "This section focuses on:"),
    (r"\bThis slide represents\b", "This section represents"),
    (r"\bThis slide references\b", "This section references"),
    (r"\bThis slide shows\b", "This section shows"),
    (r"\bThis slide builds on\b", "Building on the previous section,"),
    (r"\bThis slide brings together\b", "This section brings together"),
    (r"\bThis slide naturally leads to\b", "This connects to"),
    (r"\bThis slide is basically\b", "Think of this as"),
    (r"\bThis slide is not really about\b", "This section is not really about"),
    (r"\bThis slide is introducing\b", "This section introduces"),
    (r"\bThis slide is extremely important because\b", "This is important because"),
    (r"\bThis slide is extremely practical\.\b", "This is highly practical."),
    (r"\bThis slide is a continuation of\b", "This continues"),
    (r"\bThis slide is arguably\b", "This is arguably"),
    (r"\bThis slide is actually\b", "This is"),
    (r"\bThis slide is extremely\b", "This section is"),
    (r"\bThis slide is\b", "This section is"),
    (r"\bcybersecurity slide\b", "cybersecurity topic"),
    (r"\bon this slide\b", "in this section"),
    (r"\bat the end of this slide\b", "as a summary"),
    (r"\bParticipants will\b", "You will"),
    (r"\bparticipants will\b", "you will"),
    (r"\bParticipants may\b", "You may"),
    (r"\bparticipants may\b", "you may"),
    (r"\bParticipants see\b", "You will see"),
    (r"\bparticipants see\b", "you will see"),
    (r"\bParticipants can\b", "You can"),
    (r"\bparticipants can\b", "you can"),
    (r"\bParticipants deployed\b", "You deployed"),
    (r"\bparticipants deployed\b", "you deployed"),
    (r"\bparticipants generate\b", "you generate"),
    (r"\bstudents must understand\b", "you should understand"),
    (r"\bStudents must understand\b", "You should understand"),
    (r"\bstudents will work with\b", "you will work with"),
    (r"\bStudents will work with\b", "You will work with"),
    (r"\bstudents will\b", "you will"),
    (r"\bStudents will\b", "You will"),
    (r"\bstudents often miss\b", "you may miss"),
    (r"\bStudents often miss\b", "You may miss"),
    (r"\bstudents often\b", "you may often"),
    (r"\bStudents often\b", "You may often"),
    (r"\bteaches students\b", "covers"),
    (r"\bfor students\b", "for practice"),
    (r"\bFor students\b", "For practice"),
    (r"\bIn this course, we will learn\b", "In this course, you will learn"),
    (r"\bwe will learn\b", "you will learn"),
    (r"\bwe will work with\b", "you will work with"),
    (r"\bwe've already covered\b", "you've already covered"),
    (r"\bwe've covered\b", "you've covered"),
    (r"\byour course because students\b", "this course because you"),
    (r"\bprevious slide\b", "previous section"),
    (r"\bPrevious slide\b", "Previous section"),
    (r"\bKey Takeaway for Students\b", "Key Takeaway"),
    (r"\bRefined Instructor Notes\b", "Self-Study Notes"),
    (r"!\[Instructor Opening\]", "![Overview]"),
    (r"!\[Instructor Demonstration\]", "![Walkthrough]"),
)

def should_drop_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    return any(re.match(p, stripped, re.I) for p in DROP_LINE_PATTERNS)


def rewrite_line(line: str) -> str:
    stripped = line.strip()
    for pat, repl in LINE_REPLACEMENTS:
        m = re.match(pat, stripped, re.I)
        if m:
            return repl if "\\" not in repl else m.expand(repl)
    for pat, repl in HEADING_REPLACEMENTS:
        if re.match(pat, line):
            return repl
    return line


def rewrite_phrases(text: str) -> str:
    for pat, repl in PHRASE_REPLACEMENTS:
        text = re.sub(pat, repl, text)
    return text


def unwrap_quote(text: str) -> str:
    return text.strip().strip('"').strip("\u201c\u201d").strip()


def soften_blockquotes(lines: list[str]) -> list[str]:
    """Turn rhetorical classroom blockquotes into readable self-study lines."""
    out: list[str] = []
    reflect_mode = False
    for line in lines:
        stripped = line.strip()
        if stripped == "**Reflect:**" or stripped == "**Summary:**":
            reflect_mode = True
            out.append(line)
            continue
        if reflect_mode and not stripped:
            out.append(line)
            continue
        if reflect_mode and line.startswith(">") and not line.startswith(">>"):
            body = unwrap_quote(line.lstrip(">").strip())
            if not body:
                continue
            if body.endswith("?"):
                out.append(f"- {body}")
            else:
                out.append(body)
            continue
        if reflect_mode and stripped.startswith("#"):
            reflect_mode = False
        if stripped == "**Summary:**" and out and out[-1].strip().startswith("## Key Takeaway"):
            continue
        if line.startswith(">") and not line.startswith(">>"):
            body = unwrap_quote(line.lstrip(">").strip())
            if body and len(body) < 160:
                out.append(f"> {body}")
            else:
                out.append(line)
            continue
        out.append(line)
    return out


def cleanup_study_voice(md: str) -> str:
    md = re.sub(
        r"^This is the foundation slide for the entire course\.[^\n]*\n+",
        "",
        md,
        count=1,
        flags=re.MULTILINE,
    )
    md = re.sub(
        r"^If students understand this (?:slide|topic) properly[^\n]*\n+",
        "",
        md,
        count=1,
        flags=re.MULTILINE | re.IGNORECASE,
    )
    md = re.sub(r"\*\*Reflect:\*\*\s*>\s*[\"']?(.+?)[\"']?\s*$", r"**Reflect:**\n\n- \1", md, flags=re.MULTILINE)
    return md


def refine_to_self_study(md: str) -> str:
    md = md.replace("\r\n", "\n").replace("\r", "\n")

    lines = md.splitlines()
    lines = [rewrite_line(ln) for ln in lines if not should_drop_line(ln)]
    lines = soften_blockquotes(lines)
    md = "\n".join(lines)
    md = rewrite_phrases(md)
    md = cleanup_study_voice(md)
    md = trim_study_notes(md)
    md = collapse_blank_lines(md)
    return md


def refine_file(path: Path) -> tuple[int, int]:
    original = path.read_text(encoding="utf-8")
    refined = refine_to_self_study(original)
    path.write_text(refined, encoding="utf-8")
    return len(original.splitlines()), len(refined.splitlines())


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
        before, after = refine_file(path)
        print(f"{path.name}: {before} -> {after} lines [self-study]")


if __name__ == "__main__":
    main()
