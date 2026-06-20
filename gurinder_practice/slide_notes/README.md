# Slide Notes

Personal **self-study** notes from the **Cybersecurity in AI** course.

## Files

| | Day 1 | Day 2 |
|---|-------|-------|
| **Study notes** | [day1_study_notes.md](day1_study_notes.md) | [day2_study_notes.md](day2_study_notes.md) |
| **Speaker notes** (by slide) | [day1_speaker_notes.md](day1_speaker_notes.md) | [day2_speaker_notes.md](day2_speaker_notes.md) |
| **Diagrams** | `day1_diagrams/` (280 SVG) | `day2_diagrams/` (226 SVG) |
| **Rebuild source** | `day1_notes.md` *(local, gitignored)* | `day2_notes.md` *(local, gitignored)* |

Speaker notes align to `Cybersecurity-AI-day1.pdf` (from slide 6) and `Cybersecurity-AI-day2.pdf` (from slide 2).

## Folder layout

```
slide_notes/
├── day1_study_notes.md
├── day1_speaker_notes.md
├── day1_diagrams/
├── day2_study_notes.md
├── day2_speaker_notes.md
├── day2_diagrams/
├── day1_notes.md          ← local rebuild source (gitignored)
├── day2_notes.md
├── build_day1_study_notes.py
├── build_day2_study_notes.py
├── build_day1_speaker_notes.py
├── build_day2_speaker_notes.py
├── compact_notes.py
├── refine_self_study_notes.py
└── speaker_notes_core.py
```

## Regenerate

After editing `day1_notes.md` or `day2_notes.md`:

```bash
python gurinder_practice/slide_notes/build_day1_study_notes.py
python gurinder_practice/slide_notes/build_day2_study_notes.py
python gurinder_practice/slide_notes/build_day1_speaker_notes.py
python gurinder_practice/slide_notes/build_day2_speaker_notes.py
```

Re-apply self-study tone only:

```bash
python gurinder_practice/slide_notes/refine_self_study_notes.py
```

Diagrams render inline in GitHub and Markdown preview as `![title](day1_diagrams/*.svg)`.
