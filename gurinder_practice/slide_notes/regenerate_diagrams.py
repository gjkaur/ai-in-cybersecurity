"""Regenerate study-note diagrams as Mermaid flowcharts exported to SVG."""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from diagram_common import is_diagram_block, slugify, split_into_sections
from diagram_embed import DIAGRAM_DISPLAY_WIDTH, update_markdown_diagram_widths
from text_to_mermaid import text_diagram_to_mermaid

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "mermaid_config.json"
MERMAID_WIDTH = 960


def find_mmdc() -> list[str]:
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if not npx:
        raise RuntimeError("npx not found — install Node.js to export Mermaid SVGs.")
    return [npx, "--yes", "@mermaid-js/mermaid-cli"]


def export_mermaid(mmd: str, svg_path: Path) -> None:
    svg_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".mmd", delete=False, encoding="utf-8") as tmp:
        tmp.write(mmd)
        mmd_path = Path(tmp.name)
    try:
        cmd = [
            *find_mmdc(),
            "-i",
            str(mmd_path),
            "-o",
            str(svg_path),
            "-c",
            str(CONFIG),
            "-b",
            "transparent",
            "-w",
            str(MERMAID_WIDTH),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or result.stdout.strip() or "mmdc failed")
    finally:
        mmd_path.unlink(missing_ok=True)


def collect_diagrams(notes_path: Path, diagrams_dir: Path, mermaid_dir: Path | None) -> list[tuple[str, str, str]]:
    """Return (svg_filename, mermaid_source, alt_title) for each diagram in order."""
    md = notes_path.read_text(encoding="utf-8")
    pattern = re.compile(r"```text\n(.*?)```", re.DOTALL)
    items: list[tuple[str, str, str]] = []
    global_counter = 0

    for _title, body in split_into_sections(md):
        section_slug = slugify(_title)
        for match in pattern.finditer(body):
            text = match.group(1)
            start = match.start()
            context = body[max(0, start - 400) : start]
            if not is_diagram_block(text, context):
                continue
            global_counter += 1
            header_m = re.findall(r"^#{1,3}\s+(.+)$", context, re.MULTILINE)
            diag_title = header_m[-1].strip() if header_m else f"Diagram {global_counter}"
            if diag_title.lower().startswith("draw"):
                diag_title = "Diagram"
            svg_name = f"{section_slug}-{global_counter:03d}.svg"
            mermaid = text_diagram_to_mermaid(text, diag_title)
            items.append((svg_name, mermaid, diag_title))
            if mermaid_dir:
                (mermaid_dir / svg_name.replace(".svg", ".mmd")).write_text(mermaid, encoding="utf-8")
    return items


def study_note_diagram_targets(study_path: Path) -> list[tuple[str, str]]:
    """Return ordered (relative_svg_path, alt_text) from study markdown."""
    md = study_path.read_text(encoding="utf-8")
    return re.findall(
        r'src="((?:day\d_diagrams/)?[\w./-]+\.svg)"\s+width="\d+"\s+alt="([^"]*)"',
        md,
        flags=re.IGNORECASE,
    )


def find_diagram_texts(notes_path: Path) -> list[tuple[str, str, str]]:
    """Return (alt_title, text_block, auto_svg_name) for each diagram in notes."""
    md = notes_path.read_text(encoding="utf-8")
    pattern = re.compile(r"```text\n(.*?)```", re.DOTALL)
    found: list[tuple[str, str, str]] = []
    global_counter = 0
    for _title, body in split_into_sections(md):
        section_slug = slugify(_title)
        for match in pattern.finditer(body):
            text = match.group(1)
            start = match.start()
            context = body[max(0, start - 400) : start]
            if not is_diagram_block(text, context):
                continue
            global_counter += 1
            header_m = re.findall(r"^#{1,3}\s+(.+)$", context, re.MULTILINE)
            diag_title = header_m[-1].strip() if header_m else f"Diagram {global_counter}"
            if diag_title.lower().startswith("draw"):
                diag_title = "Diagram"
            svg_name = f"{section_slug}-{global_counter:03d}.svg"
            found.append((diag_title, text, svg_name))
    return found


def _norm_alt(value: str) -> str:
    import html

    value = html.unescape(value).lower()
    value = re.sub(r"[^\w\s]", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def map_study_targets_to_sources(
    targets: list[tuple[str, str]],
    sources: list[tuple[str, str, str]],
) -> list[tuple[str, str, str]]:
    """Map study-note svg paths to diagram text via alt-text matching."""
    unused = sources.copy()
    mapped: list[tuple[str, str, str]] = []
    for rel_path, alt in targets:
        want = _norm_alt(alt)
        best_idx = None
        best_score = 0
        for idx, (title, text, auto_name) in enumerate(unused):
            score = 0
            if _norm_alt(title) == want:
                score = 100
            elif want and want in _norm_alt(title):
                score = 80
            elif want and _norm_alt(title) in want:
                score = 70
            elif Path(rel_path).name == auto_name:
                score = 90
            if score > best_score:
                best_score = score
                best_idx = idx
        if best_idx is None and unused:
            best_idx = 0
            best_score = 1
        if best_idx is None:
            continue
        title, text, _auto = unused.pop(best_idx)
        mapped.append((rel_path, text, title))
    return mapped


def regenerate_from_study_notes(day: int) -> tuple[int, Path, Path]:
    """Regenerate diagrams referenced by study notes (used when auto names diverge)."""
    notes_path = ROOT / f"day{day}_notes.md"
    study_path = ROOT / f"day{day}_study_notes.md"
    diagrams_dir = ROOT / f"day{day}_diagrams"
    mermaid_dir = ROOT / f"day{day}_mermaid"
    if mermaid_dir.exists():
        shutil.rmtree(mermaid_dir)
    mermaid_dir.mkdir(parents=True)

    targets = study_note_diagram_targets(study_path)
    sources = find_diagram_texts(notes_path)
    mapped = map_study_targets_to_sources(targets, sources)

    items: list[tuple[str, str, str]] = []
    for rel_path, text, title in mapped:
        svg_name = Path(rel_path).name
        mermaid = text_diagram_to_mermaid(text, title)
        items.append((svg_name, mermaid, title))
        (mermaid_dir / svg_name.replace(".svg", ".mmd")).write_text(mermaid, encoding="utf-8")

    ok = 0
    failed: list[str] = []

    def _export(item: tuple[str, str, str]) -> tuple[str, bool, str]:
        svg_name, mermaid, _title = item
        try:
            export_mermaid(mermaid, diagrams_dir / svg_name)
            return svg_name, True, ""
        except Exception as exc:
            return svg_name, False, str(exc)

    workers = min(6, max(1, len(items) // 20))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_export, item) for item in items]
        for fut in as_completed(futures):
            svg_name, success, err = fut.result()
            if success:
                ok += 1
            else:
                failed.append(f"{svg_name}: {err}")

    for msg in failed[:10]:
        print(f"  WARN {msg}", file=sys.stderr)

    updated = update_markdown_diagram_widths(
        study_path.read_text(encoding="utf-8"),
        ROOT,
        DIAGRAM_DISPLAY_WIDTH,
    )
    study_path.write_text(updated, encoding="utf-8")
    return ok, diagrams_dir, study_path


def regenerate_day(day: int, keep_mermaid: bool = True) -> tuple[int, Path, Path]:
    notes_path = ROOT / f"day{day}_notes.md"
    study_path = ROOT / f"day{day}_study_notes.md"
    diagrams_dir = ROOT / f"day{day}_diagrams"
    mermaid_dir = ROOT / f"day{day}_mermaid" if keep_mermaid else None

    if not notes_path.exists():
        raise FileNotFoundError(notes_path)

    disk = {p.name for p in diagrams_dir.glob("*.svg")} if diagrams_dir.exists() else set()
    gen_names = {n for n, _, _ in collect_diagrams(notes_path, diagrams_dir, None)}
    if study_path.exists() and disk and len(disk & gen_names) < len(disk) * 0.9:
        print(f"  Using study-note path mapping (name overlap {len(disk & gen_names)}/{len(disk)})")
        return regenerate_from_study_notes(day)

    diagrams_dir.mkdir(parents=True, exist_ok=True)
    if mermaid_dir:
        if mermaid_dir.exists():
            shutil.rmtree(mermaid_dir)
        mermaid_dir.mkdir(parents=True)

    items = collect_diagrams(notes_path, diagrams_dir, mermaid_dir)
    if not items:
        raise RuntimeError(f"No diagrams found in {notes_path.name}")

    ok = 0
    failed: list[str] = []

    def _export(item: tuple[str, str, str]) -> tuple[str, bool, str]:
        svg_name, mermaid, _title = item
        svg_path = diagrams_dir / svg_name
        try:
            export_mermaid(mermaid, svg_path)
            return svg_name, True, ""
        except Exception as exc:
            return svg_name, False, str(exc)

    workers = min(6, max(1, len(items) // 20))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = [pool.submit(_export, item) for item in items]
        for fut in as_completed(futures):
            svg_name, success, err = fut.result()
            if success:
                ok += 1
            else:
                failed.append(f"{svg_name}: {err}")

    for msg in failed[:10]:
        print(f"  WARN {msg}", file=sys.stderr)
    if len(failed) > 10:
        print(f"  WARN …and {len(failed) - 10} more failures", file=sys.stderr)

    if study_path.exists():
        updated = update_markdown_diagram_widths(
            study_path.read_text(encoding="utf-8"),
            ROOT,
            DIAGRAM_DISPLAY_WIDTH,
        )
        study_path.write_text(updated, encoding="utf-8")

    return ok, diagrams_dir, study_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("days", nargs="*", type=int, default=[1, 2], help="Day numbers (default: 1 2)")
    parser.add_argument("--no-mermaid-sources", action="store_true", help="Skip writing .mmd source files")
    args = parser.parse_args()

    for day in args.days:
        print(f"Day {day}: exporting Mermaid diagrams…")
        count, diagrams_dir, study_path = regenerate_day(day, keep_mermaid=not args.no_mermaid_sources)
        print(f"  SVGs written: {count} → {diagrams_dir}")
        if study_path.exists():
            print(f"  Updated embed widths in {study_path.name} (max {DIAGRAM_DISPLAY_WIDTH}px)")


if __name__ == "__main__":
    main()
