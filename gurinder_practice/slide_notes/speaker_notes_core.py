"""Shared helpers for PDF-aligned speaker notes (Day 1 and Day 2)."""
from __future__ import annotations

import re
from pathlib import Path

import fitz

SKIP_SLIDE_PATTERNS = (
    r"^©",
    r"^\d+$",
    r"^corporation$",
    r"^virtualization$",
    r"^property$",
)


def norm(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9&]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def find_pdf(name: str, search_roots: tuple[Path, ...]) -> Path:
    for base in search_roots:
        p = base / name
        if p.exists():
            return p
    raise FileNotFoundError(f"{name} not found")


def extract_pdf_slide_title(page: fitz.Page) -> str:
    candidates: list[tuple[float, str]] = []
    for block in page.get_text("dict").get("blocks", []):
        if block.get("type") != 0:
            continue
        for line in block.get("lines", []):
            for span in line.get("spans", []):
                text = span.get("text", "").strip()
                if not text or len(text) < 4:
                    continue
                if any(re.match(p, text, re.I) for p in SKIP_SLIDE_PATTERNS):
                    continue
                if text.startswith("©") or text.isdigit():
                    continue
                candidates.append((span.get("size", 0), text))
    if not candidates:
        return "Untitled"
    candidates.sort(key=lambda x: (-x[0], -len(x[1])))
    title = candidates[0][1]
    if title.isupper():
        return title.title()
    return title


def extract_pdf_on_slide(page: fitz.Page, title: str) -> str:
    lines = [ln.strip() for ln in page.get_text().splitlines() if ln.strip()]
    body: list[str] = []
    passed = False
    for ln in lines:
        if ln.startswith("©") or re.fullmatch(r"\d+", ln):
            continue
        if not passed:
            if ln.lower() == title.lower() or (
                title.lower() in ln.lower() and len(ln) < len(title) + 8
            ):
                passed = True
            continue
        clean = ln.lstrip("•▪").strip()
        if clean and clean.lower() != title.lower():
            body.append(f"- {clean}")
    return "\n".join(body)


def trim_instructor_md(md: str, start_patterns: tuple[str, ...]) -> str:
    for pat in start_patterns:
        m = re.search(pat, md, re.MULTILINE | re.IGNORECASE)
        if m:
            return md[m.start() :]
    md = re.sub(
        r"^# Day \d+ — Refined Instructor Notes.*?(?=^## )",
        "",
        md,
        count=1,
        flags=re.DOTALL | re.MULTILINE,
    )
    md = re.sub(r"^# Day \d+ content\s*\n+", "", md, flags=re.MULTILINE)
    md = re.sub(r"^## Table of contents.*?^(?=## )", "", md, flags=re.DOTALL | re.MULTILINE)
    md = re.sub(r"^## Course flow.*?^(?=## )", "", md, flags=re.DOTALL | re.MULTILINE)
    md = re.sub(r"^## Notes\s*\n(?:- .+\n?)+\n+", "", md, flags=re.MULTILINE)
    return md.strip()


def parse_instructor_sections(md: str) -> list[tuple[str, int, str]]:
    lines = md.splitlines(keepends=True)
    indices: list[tuple[int, str, int]] = []
    for i, line in enumerate(lines):
        m = re.match(r"^(#{2,4})\s+(.+)$", line)
        if not m:
            continue
        title = re.sub(r"\s*\{#[^}]+\}", "", m.group(2).strip())
        if title in ("Table of contents", "Course flow", "Notes"):
            continue
        indices.append((i, title, len(m.group(1))))
    out: list[tuple[str, int, str]] = []
    for idx, (start, title, level) in enumerate(indices):
        end = indices[idx + 1][0] if idx + 1 < len(indices) else len(lines)
        body = "".join(lines[start + 1 : end]).strip()
        out.append((title, level, body))
    return out


def match_sections(
    sections: list[tuple[str, int, str]],
    hints: tuple[str, ...],
    used: set[str],
) -> list[tuple[str, str]]:
    matched: list[tuple[str, str]] = []
    for hint in hints:
        hint_n = norm(hint)
        for title, _level, body in sections:
            if title in used:
                continue
            t_n = norm(title)
            if hint_n in t_n or t_n in hint_n:
                matched.append((title, body))
                used.add(title)
                break
    return matched


def fallback_sections(
    sections: list[tuple[str, int, str]],
    slide_title: str,
    used: set[str],
    max_sections: int = 4,
) -> list[tuple[str, str]]:
    st = norm(slide_title)
    scored: list[tuple[int, str, str]] = []
    for title, _level, body in sections:
        if title in used or not body.strip():
            continue
        t = norm(title)
        score = 0
        for word in st.split():
            if len(word) > 3 and word in t:
                score += 2
        if score:
            scored.append((score, title, body))
    scored.sort(reverse=True)
    out: list[tuple[str, str]] = []
    for _score, title, body in scored[:max_sections]:
        out.append((title, body))
        used.add(title)
    return out


def format_notes_block(sections: list[tuple[str, str]]) -> str:
    if not sections:
        return ""
    parts: list[str] = []
    for title, body in sections:
        if not body.strip():
            continue
        body = re.sub(r"^\*§\d+/\d+ · .+\*\s*\n", "", body.strip(), flags=re.MULTILINE)
        parts.append(f"### {title}\n\n{body}\n")
    return "\n".join(parts)


def format_slide(num: int, title: str, on_slide: str, notes: str) -> str:
    out = [f"\n---\n\n## Slide {num} — {title}\n"]
    if on_slide:
        out.append("\n**On slide:**\n\n" + on_slide + "\n")
    if notes.strip():
        out.append("\n**Speaker notes:**\n\n" + notes.strip() + "\n")
    elif title.lower().startswith("pop quiz") or title.lower().startswith("lab"):
        out.append(
            "\n**Speaker notes:** Discuss the question; reveal answer after student responses.\n"
        )
    elif title.lower().startswith("congratulations"):
        out.append("\n**Speaker notes:** Close the course; recap Day 2 outcomes and next steps.\n")
    else:
        out.append(
            "\n**Speaker notes:** Expand on the on-slide bullets using your own examples.\n"
        )
    return "".join(out)


def build_speaker_notes(
    *,
    pdf_path: Path,
    instructor_path: Path,
    output_path: Path,
    day_label: str,
    pdf_label: str,
    start_slide: int,
    slide_hints: dict[int, tuple[str, ...]],
    trim_patterns: tuple[str, ...],
) -> int:
    doc = fitz.open(pdf_path)
    instructor = trim_instructor_md(
        instructor_path.read_text(encoding="utf-8"), trim_patterns
    )
    sections = parse_instructor_sections(instructor)
    used: set[str] = set()

    parts = [
        f"# {day_label} — Speaker Notes\n\n",
        f"Use with **{pdf_label}**. Each section matches one slide (from slide {start_slide}).\n",
    ]

    for i in range(start_slide - 1, doc.page_count):
        num = i + 1
        page = doc[i]
        title = extract_pdf_slide_title(page)
        on_slide = extract_pdf_on_slide(page, title)

        if title.lower().startswith("pop quiz") or title.lower().startswith("lab"):
            parts.append(format_slide(num, title, on_slide, ""))
            continue

        hints = slide_hints.get(num, (title,))
        matched = match_sections(sections, hints, used)
        if not matched:
            matched = fallback_sections(sections, title, used)
        notes = format_notes_block(matched)
        parts.append(format_slide(num, title, on_slide, notes))

    text = re.sub(r"\n{3,}", "\n\n", "".join(parts)).strip() + "\n"
    output_path.write_text(text, encoding="utf-8")
    return len(re.findall(r"^## Slide ", text, re.MULTILINE))
