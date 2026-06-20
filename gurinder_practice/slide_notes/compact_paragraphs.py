"""Convert study notes into compact paragraphs without losing content."""
from __future__ import annotations

import re
import sys
from pathlib import Path

HEADING_RE = re.compile(r"^#{1,6}\s")
BULLET_RE = re.compile(r"^(\*|-)\s+(.+)$")
ORDERED_RE = re.compile(r"^\d+\.\s+")
IMG_RE = re.compile(r"^<img\s|^\!\[")
HR_RE = re.compile(r"^---+\s*$")
MAX_BULLET_INLINE = 52
MAX_PROSE_SENTENCES = 4
MAX_PROSE_CHARS = 520

SKIP_INLINE_INTROS = {
    "from",
    "from:",
    "known as",
    "known as:",
    "this section covers",
    "this section covers:",
    "goal",
    "goal:",
    "example",
    "examples",
    "examples:",
    "record",
    "record:",
    "verify",
    "verify:",
    "backups primarily support",
    "hashes and validation support",
}


def is_structural(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    if HEADING_RE.match(s):
        return True
    if HR_RE.match(s):
        return True
    if IMG_RE.match(s):
        return True
    if s.startswith("```"):
        return True
    if s.startswith(">"):
        return True
    if s.startswith("|"):
        return True
    if BULLET_RE.match(s):
        return True
    if ORDERED_RE.match(s):
        return True
    if s.startswith("**Reflect:**") or s.startswith("**Summary:**"):
        return True
    if s.startswith("**Q:**") or s.startswith("**Answer:**"):
        return True
    return False


def is_prose(line: str) -> bool:
    s = line.strip()
    return bool(s) and not is_structural(line)


def ends_sentence(s: str) -> bool:
    return bool(re.search(r"[.!?](?:\)|\"|\')?$", s.strip()))


def join_items(items: list[str], *, lowercase: bool = False) -> str:
    cleaned = [re.sub(r"\*\*([^*]+)\*\*", r"\1", it.strip()) for it in items if it.strip()]
    if lowercase:
        cleaned = [c[0].lower() + c[1:] if c else c for c in cleaned]
    if len(cleaned) == 1:
        return cleaned[0]
    if len(cleaned) == 2:
        return f"{cleaned[0]} and {cleaned[1]}"
    return ", ".join(cleaned[:-1]) + f", and {cleaned[-1]}"


def last_nonempty(out: list[str]) -> int:
    for idx in range(len(out) - 1, -1, -1):
        if out[idx].strip():
            return idx
    return -1


def inline_bullet_block(intro: str, items: list[str]) -> str | None:
    if len(items) < 2:
        return None
    if any(len(it) > MAX_BULLET_INLINE for it in items):
        return None
    if any(it.endswith(":") for it in items):
        return None

    intro_stripped = intro.strip()
    if intro_stripped.lower().rstrip(":") in {s.rstrip(":") for s in SKIP_INLINE_INTROS}:
        return None
    if HEADING_RE.match(intro_stripped):
        return None

    body = join_items(items)
    had_colon = intro_stripped.endswith(":")
    intro = intro_stripped
    stem = intro[:-1].strip() if had_colon else intro.strip()
    low = stem.lower()

    if low.endswith(" depend on") or low.endswith(" depends on"):
        return f"{stem} {body}."
    if "practice of protecting" in low or (low.endswith("protecting") and "cybersecurity" in low):
        return f"{stem} {body}."
    if low.startswith("without"):
        return f"{stem}, {body}."
    if low in {"physical world", "digital world"}:
        return f"{stem}: {body}."
    if had_colon:
        return f"{stem}: {body}."
    return f"{stem} {body}."


def append_line(out: list[str], line: str) -> None:
    s = line.strip()
    if not s:
        if out and out[-1].strip():
            out.append("")
        return
    if HEADING_RE.match(s) and out and out[-1].strip():
        out.append("")
    out.append(line.rstrip())


def collect_bullets(lines: list[str], start: int) -> tuple[list[str], int]:
    items: list[str] = []
    k = start
    while k < len(lines):
        m = BULLET_RE.match(lines[k].strip())
        if not m:
            break
        items.append(m.group(2).strip())
        k += 1
        while k < len(lines) and not lines[k].strip():
            if k + 1 < len(lines) and BULLET_RE.match(lines[k + 1].strip()):
                k += 1
                continue
            break
    return items, k


def skip_blank(lines: list[str], k: int) -> int:
    while k < len(lines) and not lines[k].strip():
        k += 1
    return k


def chain_from_clause(sentence: str, lines: list[str], k: int) -> tuple[str, int]:
    k = skip_blank(lines, k)
    if k >= len(lines):
        return sentence, k
    label = lines[k].strip().lower().rstrip(":")
    if label != "from":
        return sentence, k
    items, k = collect_bullets(lines, skip_blank(lines, k + 1))
    if not items:
        return sentence, k
    body = join_items(items, lowercase=True)
    return sentence.rstrip(".") + f" from {body}.", k


def attach_trailing_prose(sentence: str, lines: list[str], k: int) -> tuple[str, int]:
    k = skip_blank(lines, k)
    if k >= len(lines) or not is_prose(lines[k]):
        if not sentence.endswith("."):
            sentence += "."
        return sentence, k
    trailing = lines[k].strip()
    if trailing[0].isupper():
        if not sentence.endswith("."):
            sentence += "."
        return sentence, k
    merged = sentence.rstrip(".") + " " + trailing
    if not merged.endswith("."):
        merged += "."
    return merged, k + 1


def merge_prose_lines(lines: list[str]) -> list[str]:
    out: list[str] = []
    buf: list[str] = []

    def flush() -> None:
        if not buf:
            return
        if len(buf) == 1:
            append_line(out, buf[0])
        else:
            merged = re.sub(r"\s+", " ", " ".join(buf)).strip()
            append_line(out, merged)
        buf.clear()

    for line in lines:
        s = line.strip()
        if not is_prose(line):
            flush()
            append_line(out, line)
            continue
        if s.endswith(":"):
            flush()
            append_line(out, line)
            continue
        if buf and (len(buf) >= MAX_PROSE_SENTENCES or sum(len(x) for x in buf) > MAX_PROSE_CHARS):
            flush()
        if buf and ends_sentence(buf[-1]) and s[0].isupper() and len(buf[-1]) > 100:
            flush()
        buf.append(s)

    flush()
    return out


def compact_block(lines: list[str]) -> list[str]:
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]

        if not line.strip():
            append_line(out, "")
            i += 1
            continue

        if is_structural(line) or not is_prose(line):
            append_line(out, line)
            i += 1
            continue

        intro = line.strip()
        j = skip_blank(lines, i + 1)
        items, k = collect_bullets(lines, j) if j < len(lines) else ([], j)

        if items:
            label = intro.lower().rstrip(":")
            if label == "from":
                idx = last_nonempty(out)
                if idx >= 0:
                    body = join_items(items, lowercase=True)
                    out[idx] = out[idx].rstrip(".") + f" from {body}."
                    i = k
                    sentence, i = attach_trailing_prose(out[idx], lines, i)
                    out[idx] = sentence
                    continue

            inlined = inline_bullet_block(intro, items)
            if inlined:
                sentence, k = chain_from_clause(inlined, lines, k)
                sentence, k = attach_trailing_prose(sentence, lines, k)
                append_line(out, sentence)
                i = k
                continue

        run = [line.rstrip()]
        i += 1
        while i < len(lines):
            if not lines[i].strip():
                if i + 1 < len(lines) and is_prose(lines[i + 1]) and not lines[i + 1].strip().endswith(":"):
                    i += 1
                    continue
                break
            if is_structural(lines[i]) or not is_prose(lines[i]):
                break
            if lines[i].strip().endswith(":"):
                break
            run.append(lines[i].rstrip())
            i += 1

        for ln in merge_prose_lines(run):
            if ln.strip():
                append_line(out, ln)
            elif out and out[-1].strip():
                append_line(out, "")

        if i < len(lines) and not lines[i].strip():
            i += 1

    return out


def tighten_bullet_lists(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    for idx, line in enumerate(lines):
        if not line.strip() and out:
            nxt = lines[idx + 1].strip() if idx + 1 < len(lines) else ""
            prev = out[-1].strip()
            if BULLET_RE.match(prev) and BULLET_RE.match(nxt):
                continue
            if ORDERED_RE.match(prev) and ORDERED_RE.match(nxt):
                continue
        out.append(line.rstrip())
    return "\n".join(out)


def trim_redundant_hrules(md: str) -> str:
    md = re.sub(r"\n---\n+(?=#### )", "\n\n", md)
    md = re.sub(r"\n---\n+(?=### Example )", "\n\n", md)
    return md


def compact_paragraphs(md: str) -> str:
    md = md.replace("\r\n", "\n").replace("\r", "\n")
    md = tighten_bullet_lists(md)
    lines = compact_block(md.splitlines())
    md = "\n".join(lines)
    md = trim_redundant_hrules(md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip() + "\n"


def compact_file(path: Path) -> tuple[int, int]:
    original = path.read_text(encoding="utf-8")
    compacted = compact_paragraphs(original)
    path.write_text(compacted, encoding="utf-8")
    return len(original.splitlines()), len(compacted.splitlines())


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
        before, after = compact_file(path)
        pct = 100 * (1 - after / before) if before else 0
        print(f"{path.name}: {before} -> {after} lines ({pct:.1f}% reduction)")


if __name__ == "__main__":
    main()
