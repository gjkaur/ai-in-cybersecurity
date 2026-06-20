"""Build Day 2 speaker notes aligned to Cybersecurity-AI-day2.pdf slide headings."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from speaker_notes_core import build_speaker_notes, find_pdf  # noqa: E402

STUDY_NOTES = ROOT / "day2_study_notes.md"
OUTPUT = ROOT / "day2_speaker_notes.md"

PDF_SEARCH = (ROOT.parents[2], ROOT.parents[1], ROOT)

# Slide number -> keywords to match ## / ### headings in instructor notes
SLIDE_NOTE_HINTS: dict[int, tuple[str, ...]] = {
    2: (
        "From Detection to Investigation",
        "Day 1 Foundation",
        "Day 2 Focus Areas",
        "What Participants Will Learn",
    ),
    3: (
        "What You Will Build Today",
        "Lab 2.2",
        "Lab 2.3",
        "Lab 2.4",
        "End-of-Day Outcome",
    ),
    4: (
        "Security Information and Event Management",
        "Why SIEM Systems Exist",
        "Core SIEM Functions",
        "Typical SIEM Architecture",
    ),
    5: (
        "Example SIEM Investigation",
        "Common SIEM Data Sources",
        "SIEM in the SOC Workflow",
        "Breaking Down SIEM",
    ),
    6: (
        "Cloud-Native Monitoring vs. Traditional SIEMs",
        "Traditional SIEM Architecture",
        "Cloud-Native Monitoring Architecture",
    ),
    7: (
        "Amazon CloudWatch — Architecture Overview",
        "CloudWatch Architecture",
        "Data Sources",
    ),
    8: (
        "Core CloudWatch Components",
        "CloudWatch Operational Workflow",
        "CloudWatch for Security Operations",
    ),
    9: (
        "The CloudWatch Agent and Log Ingestion",
        "Why the CloudWatch Agent Exists",
        "What is the CloudWatch Agent?",
    ),
    10: (
        "Log Ingestion Workflow",
        "Log Group and Log Stream",
        "Centralized Log Ingestion",
    ),
    11: (
        "CloudWatch Logs Insights — Query Language",
        "Why Logs Insights Matters",
        "Query Structure",
        "Security Investigation Example 1",
    ),
    12: (
        "AI-Powered Query Generation in CloudWatch",
        "Why AWS Added AI Query Generation",
        "Example 1 — Failed SSH Logins",
    ),
    13: (
        "Human-in-the-Loop Model",
        "Best Practices for Using AI Query Generation",
        "Step 3 — Review the Generated Query",
    ),
    14: (
        "CloudWatch AI Operations — What It Is",
        "What Is CloudWatch AI Operations?",
        "Core Capabilities",
    ),
    15: (
        "Investigation Hypotheses and Analyst Review",
        "What Is a Hypothesis?",
        "AI Investigation Process",
    ),
    16: (
        "How AI Investigations Work",
        "High-Level Investigation Pipeline",
        "Step 1: Define the Scope",
        "Step 2: Evidence Collection",
    ),
    17: (
        "Human-in-the-Loop Review",
        "Example Investigation Walkthrough",
        "Benefits of AI-Assisted Investigations",
    ),
    18: (
        "Signal vs. Noise in Log Data",
        "Understanding Signal and Noise",
        "Why Noise Creates Problems",
    ),
    19: (
        "Common Sources of Noise",
        "How AI Helps Reduce Noise",
        "Analyst Best Practice",
    ),
    20: (
        "MITRE ATT&CK Mapping in Investigations",
        "Why ATT&CK Mapping Helps",
    ),
    21: (
        "MITRE ATT&CK Mapping in Investigations — Common Techniques",
        "Example Detection Workflow",
    ),
    22: (
        "IAM Roles for CloudWatch Access",
        "Why IAM Roles Matter",
    ),
    23: (
        "IAM Roles for CloudWatch Access — Required Roles",
        "Least Privilege",
    ),
    24: (
        "Log Retention and Investigation Retention",
        "Why Retention Matters",
    ),
    25: (
        "Investigation Retention",
        "Log Retention Policies",
    ),
    26: (
        "Evaluating AI-Generated Hypotheses",
        "Analyst Validation Framework",
    ),
    27: (
        "Evaluating AI-Generated",
        "Human Review",
        "Limitations",
    ),
    33: (
        "What Is a SOC Dashboard?",
        "What is the Purpose of a SOC Dashboard?",
    ),
    34: (
        "Three-Panel SOC Dashboard",
        "Dashboard Components",
    ),
    35: (
        "Step 2: Metric Filters",
        "Why Metric Filter Design Matters",
        "Pattern Type 1",
    ),
    36: (
        "Metric Filter",
        "SSH Failure Detection",
        "Privilege Escalation Detection",
    ),
    37: (
        "Writing Effective Metric Filter",
        "Testing Checklist",
        "SOC Design Recommendation",
    ),
    38: (
        "What Is a CloudWatch Alarm?",
        "Alarm States",
        "Alarm Components",
    ),
    39: (
        "Key Configuration Decision",
        "Threshold",
        "Evaluation Periods",
        "Alarm Tuning Strategy",
    ),
    40: (
        "What is a Runbook?",
        "Why Runbooks Matter",
        "Runbook Section 1",
    ),
    41: (
        "Connecting Alarms to AI",
        "Automated AI Workflow",
        "Why Connect Alarms to AI Operations",
    ),
    42: (
        "Privilege Escalation Detection",
        "Understanding `sudo`",
        "MITRE ATT&CK Mapping",
    ),
    43: (
        "Detection Signal 3",
        "SetUID",
        "Audit Logs Matter",
    ),
    44: (
        "What is a Red Team?",
        "What is a Purple Team?",
        "Purple Team Goal",
    ),
    45: (
        "Test Attacker Account",
        "Why Create a Test Attacker Account?",
        "Lab Objective",
    ),
    46: (
        "Dashboard Design for Security",
        "Three-Panel SOC Dashboard",
    ),
    47: (
        "Dashboard Design",
        "Security Operations Perspective",
    ),
    48: (
        "CloudWatch Dashboard Widgets",
        "Dashboard Widgets",
    ),
    49: (
        "What Is a Detection Pipeline?",
        "Full Detection Pipeline",
        "Step 1: Logs",
    ),
    50: (
        "ATT&CK Techniques",
        "Example Attack Scenarios",
    ),
    51: (
        "Testing and Validating",
        "Validation",
        "Testing Checklist",
    ),
    52: (
        "Testing and Validating",
        "SOC Best Practice",
    ),
    60: (
        "Detection Engineering",
        "Detection Engineering Mindset",
        "What Does a Detection Engineer",
    ),
    61: (
        "Detection Engineering vs Incident Response",
        "Detection Engineer",
    ),
    62: (
        "Choosing What To Detect",
        "Threat Prioritization",
    ),
    63: (
        "Choosing What To Detect",
        "Coverage",
    ),
    64: (
        "Linux Endpoint Threat Catalog",
        "Threat Catalog",
    ),
    65: (
        "Auditd",
        "Linux Audit Daemon",
        "Why Auditd",
    ),
    66: (
        "audit rules",
        "Auditd Configuration",
    ),
    67: (
        "File Permission",
        "Access Monitoring",
    ),
    68: (
        "Permission Changes",
        "File Integrity",
    ),
    69: (
        "Designing A Detection",
        "From Idea to Rule",
        "Detection Rule",
    ),
    70: (
        "Designing A Detection",
        "Detection Workflow",
    ),
    71: (
        "Simulating Attacks Safely",
        "Purple Team",
    ),
    72: (
        "Simulating Attacks",
        "Test Attacker",
    ),
    73: (
        "Reading Auditd Log Entries",
        "audit.log",
    ),
    74: (
        "Reading Auditd",
        "Parse audit",
    ),
    75: (
        "Incident Reporting — Structure",
        "Investigation Report",
        "Structured Incident Report",
    ),
    76: (
        "Incident Reporting",
        "Executive Summary",
        "Investigation Evidence",
    ),
    77: (
        "Final Message",
        "Course Takeaway",
        "Investigation Closure",
    ),
    78: (
        "AI Hypothesis Triage",
        "Hypothesis Triage",
        "Evaluating AI-Generated",
    ),
    79: (
        "Detection Coverage and Gaps",
        "Coverage Gap",
    ),
    80: (
        "Detection Coverage",
        "ATT&CK coverage",
    ),
    81: (
        "Closing An Investigation",
        "Investigation Closure and Detection Improvement",
    ),
    89: (
        "Final Message",
        "Course Takeaway",
        "Congratulations",
    ),
}


def main() -> None:
    if not STUDY_NOTES.exists():
        raise SystemExit(f"Study notes not found: {STUDY_NOTES}")
    pdf = find_pdf("Cybersecurity-AI-day2.pdf", PDF_SEARCH)
    count = build_speaker_notes(
        pdf_path=pdf,
        instructor_path=STUDY_NOTES,
        output_path=OUTPUT,
        day_label="Day 2",
        pdf_label="Cybersecurity-AI-day2.pdf",
        start_slide=2,
        slide_hints=SLIDE_NOTE_HINTS,
        trim_patterns=(
            r"^## From Detection to Investigation",
            r"^# From Detection to Investigation",
        ),
    )
    print(f"Built: {OUTPUT}")
    print(f"  Slides: {count}")


if __name__ == "__main__":
    main()
