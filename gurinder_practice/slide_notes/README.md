# Slide Notes

Personal **self-study** notes from the **Cybersecurity in AI** course.

## Files

| | Day 1 | Day 2 |
|---|-------|-------|
| **Study notes** | [day1_study_notes.md](day1_study_notes.md) | [day2_study_notes.md](day2_study_notes.md) |
| **Speaker notes** (by slide) | [day1_speaker_notes.md](day1_speaker_notes.md) | [day2_speaker_notes.md](day2_speaker_notes.md) |
| **Diagrams (SVG)** | `day1_diagrams/` | `day2_diagrams/` |
| **Mermaid sources** | `day1_mermaid/` | `day2_mermaid/` |
| **Rebuild source** | `day1_notes.md` *(local, gitignored)* | `day2_notes.md` *(local, gitignored)* |

Speaker notes align to `Cybersecurity-AI-day1.pdf` (from slide 6) and `Cybersecurity-AI-day2.pdf` (from slide 2).

Study notes use the same slide headings (`## Slide N — Title`) with self-study content grouped underneath.

## Regenerate diagrams

Diagrams are **Mermaid flowcharts** exported to SVG via `@mermaid-js/mermaid-cli`. Study notes embed them at **420px** width (readable on GitHub without being oversized).

Requires Node.js (`npx`).

```bash
cd gurinder_practice/slide_notes
python regenerate_diagrams.py
```

Regenerate one day only:

```bash
python regenerate_diagrams.py 1
python regenerate_diagrams.py 2
```

After editing `day1_notes.md` / `day2_notes.md`, re-run the script. It reads ` ```text ` diagram blocks, converts them to Mermaid, writes `.mmd` sources under `dayN_mermaid/`, exports SVGs to `dayN_diagrams/`, and updates `<img width="…">` in the study notes.

To change display size, edit `DIAGRAM_DISPLAY_WIDTH` in `diagram_embed.py` and re-run `regenerate_diagrams.py`.

## PowerPoint presenter notes

```bash
python add_pptx_speaker_notes.py <input.pptx> <output.pptx> day1_study_notes.md
```

Acronym expansion for speaker notes lives in `abbreviations.py`.
