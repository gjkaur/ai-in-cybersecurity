# Slide Notes

Personal study notes from the **Cybersecurity in AI** course slides.

## Day 1

**Deck:** `Cybersecurity-AI-day1/` (96 slides)

→ **[Day 1 — Instructor Notes](day1/day1_instructor_notes.md)** *(compact single file, full coverage)*

Organized from [`day1_notes.md`](day1_notes.md): table of contents, 30 topic parts, diagrams as click-to-open SVG links.

| Section | Slides | Topics |
|---------|--------|--------|
| Intro | 1–5 | Course logistics, instructor, prerequisites |
| Foundations | 6–10 | Cybersecurity, CIA triad, cloud perimeter |
| AWS & EC2 | 11–23 | IAM, VPC, EC2, SSH, Linux, nginx |
| Pop quizzes | 24–29 | SSH, permissions, security groups |
| Lab 1.1 | 30 | Instance setup |
| SOC & detection | 31–44 | Kill chain, ATT&CK, logs, risk scoring |
| Pop quizzes | 45–50 | T1110, risk scoring |
| Lab 1.2 | 51 | Suspicious activity simulation |
| AI in security | 52–65 | Prompts, IAM, least privilege, validation |
| Pop quizzes | 66–71 | IAM / Lambda policies |
| Lab 1.3 | 72 | AI-assisted scripting & IAM review |
| CSPM & AWS security | 73–89 | Security Hub, GuardDuty, S3, remediation |
| Pop quizzes | 90–95 | Security Hub, MFA, security groups |
| Lab 1.4 | 96 | Security posture baseline |

## Day 2

**Deck:** Day 2 — From Detection to Investigation

→ **[Day 2 — Instructor Notes](day2/day2_instructor_notes.md)** *(compact single file, full coverage)*

Organized from [`day2_notes.md`](day2_notes.md): table of contents, 22 topic parts, diagrams as click-to-open SVG links.

| Block | Topics |
|-------|--------|
| Day 2 overview | Detection → investigation, labs preview |
| SIEM & cloud monitoring | SIEM, cloud-native vs traditional SIEM |
| Amazon CloudWatch | Architecture, agent, Logs Insights |
| CloudWatch AI Operations | AI investigations, signal vs noise |
| Labs 2.2–2.4 | SOC dashboard, detection pipeline capstone |
| Detection engineering | ATT&CK, purple team, detection-as-code |

### Source notes (raw)

- [`day1_notes.md`](day1_notes.md)
- [`day2_notes.md`](day2_notes.md)

Regenerate after editing the source, then compact:

```bash
python gurinder_practice/slide_notes/day1/build_refined_notes.py
python gurinder_practice/slide_notes/day2/build_refined_notes.py
python gurinder_practice/slide_notes/compact_instructor_notes.py
```

---

*Generated from course slide images.*
