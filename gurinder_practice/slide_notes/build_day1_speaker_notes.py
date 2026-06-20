"""Build Day 1 speaker notes aligned to Cybersecurity-AI-day1.pdf slide headings."""
from __future__ import annotations

import importlib.util
import re
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parent
STUDY_NOTES = ROOT / "day1_study_notes.md"
OUTPUT = ROOT / "day1_speaker_notes.md"

SKIP_SLIDE_PATTERNS = (
    r"^©",
    r"^\d+$",
    r"^corporation$",
    r"^virtualization$",
    r"^property$",
)

# Slide number -> keywords to match ## / ### headings in instructor notes (first match wins)
SLIDE_NOTE_HINTS: dict[int, tuple[str, ...]] = {
    6: ("Instructor Opening", "Formal Definition", "Simple Definition", "Why Cybersecurity Exists", "Real World Examples"),
    7: ("What is the CIA Triad", "1. Confidentiality", "2. Integrity", "3. Availability", "Security Controls Map to CIA", "Key Takeaway for Students"),
    8: ("Threat Landscape", "Attack Surface", "Ransomware", "Credential Theft", "Supply Chain", "Cloud Misconfigurations", "Key Takeaway"),
    9: ("New Perimeter", "Castle-and-Moat", "Identity is the New Firewall", "Traditional Office"),
    10: ("Shared Responsibility", "Provider responsibility", "Customer responsibility"),
    11: ("AWS and Cloud Infrastructure", "What is AWS", "Why AWS Matters", "Core AWS Services"),
    12: ("Region", "Availability Zone", "IAM", "VPC"),
    13: ("EC2", "Connecting Everything", "Where is the resource"),
    14: ("Virtual Machines", "What is an EC2", "AMI"),
    15: ("Launching EC2", "Checklist", "Security Group", "Key Pair"),
    16: ("SSH", "Secure Shell", "Why SSH Matters"),
    17: ("SSH Key", "Key-Based Authentication", "public key", "private key"),
    18: ("Linux Filesystem", "Navigating", "pwd", "cd", "ls"),
    19: ("File Permissions", "chmod", "rwx"),
    20: ("SetUID", "Privilege Risk", "suid"),
    21: ("Finding and Investigating SetUID", "Investigating SetUID"),
    22: ("Security Groups", "Firewalls", "Inbound", "Outbound"),
    23: ("Web Service", "Nginx", "nginx", "Running and Securing"),
    31: ("SOC Analyst", "SOC Team", "What Does a SOC"),
    32: ("Cyber Kill Chain", "Reconnaissance", "Weaponization"),
    33: ("Delivery", "Exploitation", "Installation", "Command and Control", "Actions on Objectives", "Actions on Objective"),
    34: ("MITRE ATT&CK", "ATT&CK"),
    35: ("Brute Force", "T1110", "Credential Attacks"),
    36: ("Privilege Escalation", "T1548"),
    37: ("Logs Are the Foundation", "Why Logs"),
    38: ("journald", "auditd", "Linux Logging"),
    39: ("Collecting SSH Evidence", "SSH Evidence"),
    40: ("Analyst Workflow", "Evidence and the Analyst"),
    41: ("Risk Scoring", "Risk Score"),
    42: ("Risk Scoring", "Python", "Automation"),
    43: ("Python", "Security Automation", "Triage"),
    44: ("Triage", "Documentation"),
    52: ("AI in Cybersecurity", "Overview"),
    53: ("AI in Cybersecurity", "Overview", "Limitations"),
    54: ("Coding Assistants", "AI Coding"),
    55: ("Prompt Engineering", "Prompt"),
    56: ("Validating AI Output", "Reviewing and Validating"),
    57: ("IAM Fundamentals", "What is IAM"),
    58: ("IAM Policy Structure", "Policy Structure"),
    59: ("Least Privilege", "Principle of Least Privilege"),
    60: ("Least Privilege", "Lambda"),
    61: ("Lambda Execution", "Execution Roles"),
    62: ("S3 Resource", "Resource-Level Access"),
    63: ("Detecting IAM Misconfigurations", "IAM Misconfiguration"),
    64: ("Human-in-the-Loop", "Human in the Loop"),
    65: ("AI Limitations", "Limitations in Security"),
    72: ("Cloud Security Posture", "CSPM", "What is CSPM"),
    73: ("CSPM", "Posture Management"),
    74: ("Security Services Overview", "AWS Security Services"),
    75: ("Security Hub", "AWS Security Hub"),
    76: ("Security Hub", "Finding Aggregation", "GuardDuty", "Inspector"),
    77: ("GuardDuty", "Amazon GuardDuty"),
    78: ("Root Account", "MFA", "Root User"),
    79: ("Credential Hygiene", "Access Keys", "IAM Credential"),
    80: ("Security Groups", "Network Exposure"),
    81: ("Security Groups", "Network Exposure", "SSH"),
    82: ("S3 Bucket Security", "S3 Security", "Public Access"),
    83: ("CloudTrail", "Audit Logging"),
    84: ("Finding Prioritization", "Severity"),
    85: ("Controlled Remediation", "Remediation Principles"),
    86: ("Controlled Remediation", "Remediation"),
    87: ("Continuous Compliance", "Compliance Monitoring"),
    88: ("Security Findings Baseline", "Findings Baseline", "Building A Security Findings"),
}


def norm(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9&]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def find_pdf() -> Path:
    for base in (ROOT.parents[3], ROOT.parents[2], ROOT.parents[1]):
        p = base / "Cybersecurity-AI-day1.pdf"
        if p.exists():
            return p
    raise FileNotFoundError("Cybersecurity-AI-day1.pdf not found")


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
            if ln.lower() == title.lower() or (title.lower() in ln.lower() and len(ln) < len(title) + 8):
                passed = True
            continue
        clean = ln.lstrip("•▪").strip()
        if clean and clean.lower() != title.lower():
            body.append(f"- {clean}")
    return "\n".join(body)


def parse_instructor_sections(md: str) -> list[tuple[str, int, str]]:
    """Return (heading, level, body) for each ## / ### / #### block."""
    lines = md.splitlines(keepends=True)
    indices: list[tuple[int, str, int]] = []
    for i, line in enumerate(lines):
        m = re.match(r"^(#{2,4})\s+(.+)$", line)
        if m:
            indices.append((i, m.group(2).strip(), len(m.group(1))))
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
        parts.append(f"### {title}\n\n{body.strip()}\n")
    return "\n".join(parts)


def format_slide(num: int, title: str, on_slide: str, notes: str) -> str:
    out = [f"\n---\n\n## Slide {num} — {title}\n"]
    if on_slide:
        out.append("\n**On slide:**\n\n" + on_slide + "\n")
    if notes.strip():
        out.append("\n**Speaker notes:**\n\n" + notes.strip() + "\n")
    elif title.lower().startswith("pop quiz") or title.lower().startswith("lab"):
        out.append("\n**Speaker notes:** Discuss the question; reveal answer after student responses.\n")
    else:
        out.append("\n**Speaker notes:** Expand on the on-slide bullets using your own examples.\n")
    return "".join(out)


def build(start_slide: int = 6) -> str:
    pdf = find_pdf()
    doc = fitz.open(pdf)
    study_notes = STUDY_NOTES.read_text(encoding="utf-8")
    sections = parse_instructor_sections(study_notes)
    used: set[str] = set()

    parts = [
        "# Day 1 — Speaker Notes\n\n",
        "Use with **Cybersecurity-AI-day1.pdf**. Each section matches one slide (from slide 6).\n",
    ]

    for i in range(start_slide - 1, doc.page_count):
        num = i + 1
        page = doc[i]
        title = extract_pdf_slide_title(page)
        on_slide = extract_pdf_on_slide(page, title)

        if title.lower().startswith("pop quiz") or title.lower().startswith("lab"):
            parts.append(format_slide(num, title, on_slide, ""))
            continue

        hints = SLIDE_NOTE_HINTS.get(num, (title,))
        matched = match_sections(sections, hints, used)
        if not matched:
            matched = fallback_sections(sections, title, used)
        notes = format_notes_block(matched)
        parts.append(format_slide(num, title, on_slide, notes))

    text = re.sub(r"\n{3,}", "\n\n", "".join(parts)).strip() + "\n"
    return text


def main() -> None:
    if not STUDY_NOTES.exists():
        raise SystemExit(f"Study notes not found: {STUDY_NOTES}")
    OUTPUT.write_text(build(), encoding="utf-8")
    slide_count = len(re.findall(r"^## Slide ", OUTPUT.read_text(encoding="utf-8"), re.MULTILINE))
    print(f"Built: {OUTPUT}")
    print(f"  Slides: {slide_count}")


if __name__ == "__main__":
    main()
