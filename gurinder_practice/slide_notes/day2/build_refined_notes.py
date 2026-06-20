"""Build refined Day 2 slide notes: single organized file + text-diagram → SVG."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT.parent / "day2_notes.md"
DIAGRAMS = ROOT / "diagrams"
OUTPUT = ROOT / "README.md"

# Reuse diagram renderer and markdown utilities from Day 1 builder
_D1 = ROOT.parent / "day1" / "build_refined_notes.py"
_spec = importlib.util.spec_from_file_location("day1_build", _D1)
_core = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(_core)

process_diagrams = _core.process_diagrams
demote_headings = _core.demote_headings
compress_markdown = _core.compress_markdown
slugify = _core.slugify

COURSE_BLOCKS = [
    {
        "name": "Day 2 Overview",
        "topics": [
            "From Detection to Investigation — Day 2 Overview",
            "What You Will Build Today",
        ],
    },
    {
        "name": "SIEM & Cloud Monitoring",
        "topics": [
            "What is a Security Information and Event Management (SIEM) System?",
            "SIEM (Security Information and Event Management)",
            "Cloud-Native Monitoring vs. Traditional SIEMs",
        ],
    },
    {
        "name": "Amazon CloudWatch",
        "topics": [
            "Amazon CloudWatch — Architecture Overview",
            "Amazon CloudWatch — Key Components",
            "The CloudWatch Agent and Log Ingestion",
            "The CloudWatch Agent and Log Ingestion Process",
            "CloudWatch Logs Insights — Query Language",
        ],
    },
    {
        "name": "CloudWatch AI Operations",
        "topics": [
            "CloudWatch AI Operations — What It Is",
            "CloudWatch AI Operations — Investigation Hypotheses and Analyst Review",
            "Signal vs. Noise in Log Data — Common Sources of Noise",
        ],
    },
    {
        "name": "Labs 2.2–2.4",
        "topics": [
            "What Is a CloudWatch Alarm?",
            "What is a Runbook?",
            "Lab Objective",
            "What is the Purpose of a SOC Dashboard?",
            "What Is a Detection Pipeline?",
        ],
    },
    {
        "name": "Detection Engineering",
        "topics": [
            "The Detection Engineering Mindset",
            "AI Investigation Section",
            "Investigation Closure and Detection Improvement",
        ],
    },
    {
        "name": "Course Close",
        "topics": [
            "Final Message",
            "Course Takeaway",
        ],
    },
]

EXTRA_PART_STARTS = (
    "Investigation Lifecycle",
    "Investigation Workflow Overview",
    "Detection Strategy",
    "What is a Red Team?",
    "What is a Purple Team?",
    "The Three-Panel SOC Dashboard",
    "Detection Engineering vs Incident Response",
)


def is_day2_part_header(title: str) -> bool:
    if title.startswith("Key Takeaway"):
        return False
    if re.match(r"^(Command|Step|Example) \d+ —", title):
        return False
    if title.startswith("MITRE ATT&CK Mapping in Investigations — Common"):
        return False

    if " — " in title:
        return True

    return title.startswith(EXTRA_PART_STARTS) or title.startswith(
        (
            "From Detection to Investigation",
            "What You Will Build Today",
            "What is a Security Information and Event Management",
            "SIEM (Security Information and Event Management)",
            "Cloud-Native Monitoring vs",
            "Final Message",
            "Course Takeaway",
        )
    )


def split_into_sections(content: str) -> list[tuple[str, str]]:
    lines = content.splitlines(keepends=True)
    indices: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        if line.startswith("# ") and is_day2_part_header(line[2:].strip()):
            indices.append((i, line[2:].strip()))

    if not indices:
        return [("day2-notes", content)]

    sections: list[tuple[str, str]] = []
    for idx, (start, title) in enumerate(indices):
        end = indices[idx + 1][0] if idx + 1 < len(indices) else len(lines)
        body = "".join(lines[start:end]).strip() + "\n"
        sections.append((title, body))
    return sections


def infer_block(title: str) -> str:
    for block in COURSE_BLOCKS:
        for topic in block["topics"]:
            if title == topic or title.startswith(topic[:40]):
                return block["name"]
        for prefix in block.get("topics_prefix", []):
            if title.startswith(prefix):
                return block["name"]
    upper = title.upper()
    if "CLOUDWATCH" in upper and "AI" in upper:
        return "CloudWatch AI Operations"
    if "CLOUDWATCH" in upper or "LOGS INSIGHTS" in upper:
        return "Amazon CloudWatch"
    if "SIEM" in upper or "MONITORING" in upper:
        return "SIEM & Cloud Monitoring"
    if "DETECTION" in upper or "ATT&CK" in upper or "PURPLE" in upper or "RED TEAM" in upper:
        return "Detection Engineering"
    if "DASHBOARD" in upper or "LAB" in upper or "ALARM" in upper or "RUNBOOK" in upper:
        return "Labs 2.2–2.4"
    if "INVESTIGATION" in upper:
        return "CloudWatch AI Operations"
    if "FINAL" in upper or "COURSE TAKEAWAY" in upper:
        return "Course Close"
    return "Day 2 topics"


def build_master_toc(section_meta: list[tuple[int, str, str]]) -> str:
    topic_to_block: dict[str, str] = {}
    for block in COURSE_BLOCKS:
        for t in block.get("topics", []):
            topic_to_block[t] = block["name"]

    lines = ["## Table of contents\n"]
    for idx, title, anchor in section_meta:
        block = topic_to_block.get(title, infer_block(title))
        short = title if len(title) <= 62 else title[:59] + "..."
        lines.append(f"{idx}. [{short}](#{anchor}) — *{block}*")
    return "\n".join(lines) + "\n"


def build_doc_intro(section_meta: list[tuple[int, str, str]]) -> str:
    return "\n".join(
        [
            "# Day 2 — Refined Instructor Notes\n",
            "Readable, organized coverage of **Cybersecurity in AI** Day 2. ",
            "All content from [`day2_notes.md`](../day2_notes.md) is preserved in this single file; ",
            "diagrams are rendered as SVG inline.\n",
            "---\n",
            build_master_toc(section_meta),
            "---\n",
            "## Course flow\n",
            "| Block | Topics |",
            "|-------|--------|",
            "| Day 2 overview | Detection → investigation pipeline, labs 2.2–2.4 preview |",
            "| SIEM & cloud monitoring | SIEM fundamentals, cloud-native vs traditional SIEM |",
            "| Amazon CloudWatch | Architecture, agent, log ingestion, Logs Insights |",
            "| CloudWatch AI Operations | AI-assisted queries, investigations, signal vs noise |",
            "| Labs 2.2–2.4 | Alarms, runbooks, SOC dashboard, detection pipeline capstone |",
            "| Detection engineering | ATT&CK mapping, purple team, detection-as-code |",
            "| Course close | Final message and course takeaway |",
            "\n---\n",
            "## Notes\n",
            "- **Key Takeaway** blocks are slide closers; lab sections use `## Lab 2.x` headings.\n",
            "- Diagrams appear as SVG images inline.\n",
            "- Regenerate after editing `day2_notes.md`: "
            "`python gurinder_practice/slide_notes/day2/build_refined_notes.py`\n",
            "\n---\n",
            "# Day 2 content\n",
        ]
    )


def reorganize_section_body(body: str) -> str:
    """Drop duplicate H1 title; part heading replaces it."""
    return re.sub(r"^# .+\n+", "", body, count=1, flags=re.MULTILINE)


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"Source not found: {SRC}")

    raw = SRC.read_text(encoding="utf-8")
    DIAGRAMS.mkdir(parents=True, exist_ok=True)

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
        _core.DIAGRAMS = DIAGRAMS  # ensure SVG output goes to day2/diagrams/
        body = process_diagrams(body, slug, global_counter)
        body = demote_headings(body, 1)
        block = infer_block(title)
        part_header = f"\n---\n\n## {title} {{#{anchor}}}\n*Part {idx} of {len(parts)} · {block}*\n\n"
        content_parts.append(part_header + body.strip() + "\n")

    doc = build_doc_intro(section_meta) + "".join(content_parts)
    doc += (
        "\n---\n\n"
        "*Generated from [`day2_notes.md`](../day2_notes.md). "
        "Edit the source and rebuild — do not edit this file by hand.*\n"
    )
    doc = compress_markdown(doc)
    OUTPUT.write_text(doc, encoding="utf-8")

    print(f"Built single file: {OUTPUT}")
    print(f"  Topics: {len(section_meta)}, SVG diagrams: {global_counter[0]}")
    print(f"  Diagrams: {DIAGRAMS}")


if __name__ == "__main__":
    main()
