"""Convert parsed text diagrams to Mermaid flowcharts."""
from __future__ import annotations

import re

from diagram_common import parse_diagram_rows


def _quote(label: str) -> str:
    return label.replace('"', "#quot;")


def _node_id(counter: list[int], label: str) -> str:
    counter[0] += 1
    slug = re.sub(r"[^a-zA-Z0-9]", "", label)[:24] or "node"
    return f"n{counter[0]}_{slug}"


def _add_node(lines: list[str], counter: list[int], label: str, style: str = "") -> str:
    nid = _node_id(counter, label)
    lines.append(f'    {nid}["{_quote(label)}"]')
    if style:
        lines.append(f"    style {nid} {style}")
    return nid


def rows_to_mermaid(rows: list[str | list[str]], title: str = "") -> str:
    counter = [0]
    out: list[str] = ["flowchart TB"]
    clean_title = title.strip()
    if clean_title and clean_title.lower() not in {"draw", "diagram", "whiteboard diagram"}:
        tid = _add_node(out, counter, clean_title)
        out.append(f"    classDef titleNode fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#0F172A")
        out.append(f"    style {tid} fill:#EFF6FF,stroke:#2563EB,stroke-width:2px,color:#0F172A")

    i = 0
    last_nodes: list[str] = []

    def style_primary(nid: str) -> None:
        out.append(f"    style {nid} fill:#FFFFFF,stroke:#93C5FD,stroke-width:2px,color:#0F172A")

    def style_secondary(nid: str) -> None:
        out.append(f"    style {nid} fill:#ECFDF5,stroke:#86EFAC,stroke-width:2px,color:#0F172A")

    while i < len(rows):
        row = rows[i]

        if row == "GAP":
            i += 1
            continue

        if row == "ARROW":
            i += 1
            continue

        if isinstance(row, list):
            row_nodes = [_add_node(out, counter, lbl) for lbl in row]
            for nid in row_nodes:
                style_primary(nid)
            if len(last_nodes) == 1:
                for nid in row_nodes:
                    out.append(f"    {last_nodes[0]} --> {nid}")
            elif len(row_nodes) > 1:
                for a, b in zip(row_nodes, row_nodes[1:]):
                    out.append(f"    {a} --- {b}")
            last_nodes = row_nodes[-1:]
            i += 1
            if i < len(rows) and isinstance(rows[i], list):
                row2 = rows[i]
                row2_nodes = [_add_node(out, counter, lbl) for lbl in row2]
                for nid in row2_nodes:
                    style_secondary(nid)
                if len(row_nodes) == len(row2_nodes):
                    for parent, child in zip(row_nodes, row2_nodes):
                        out.append(f"    {parent} --> {child}")
                else:
                    anchor = row_nodes[len(row_nodes) // 2]
                    for nid in row2_nodes:
                        out.append(f"    {anchor} --> {nid}")
                last_nodes = row2_nodes
                i += 1
            continue

        run: list[str] = []
        j = i
        while j < len(rows) and isinstance(rows[j], str) and rows[j] not in ("GAP", "ARROW"):
            run.append(rows[j])
            if j + 1 < len(rows) and rows[j + 1] == "ARROW":
                break
            j += 1

        if len(run) >= 3 and (j >= len(rows) or rows[j] != "ARROW"):
            panel_id = _node_id(counter, "panel")
            out.append(f"    subgraph {panel_id} [ ]")
            panel_nodes = []
            for lbl in run:
                nid = _add_node(out, counter, lbl)
                style_primary(nid)
                panel_nodes.append(nid)
            for a, b in zip(panel_nodes, panel_nodes[1:]):
                out.append(f"        {a} --> {b}")
            out.append("    end")
            last_nodes = [panel_nodes[-1]]
            i = j
            continue

        chain_nodes: list[str] = []
        k = i
        while k < len(rows):
            cur = rows[k]
            if cur == "GAP":
                k += 1
                continue
            if cur == "ARROW":
                k += 1
                continue
            if isinstance(cur, list):
                break
            if isinstance(cur, str):
                nid = _add_node(out, counter, cur)
                style_primary(nid)
                chain_nodes.append(nid)
            k += 1
            if k < len(rows) and rows[k] == "ARROW":
                k += 1
                continue
            if k < len(rows) and isinstance(rows[k], list):
                break
            if k < len(rows) and isinstance(rows[k], str):
                continue
            break

        for a, b in zip(chain_nodes, chain_nodes[1:]):
            out.append(f"    {a} --> {b}")

        if chain_nodes:
            root = chain_nodes[-1]
            if k < len(rows) and isinstance(rows[k], list):
                child_nodes = [_add_node(out, counter, lbl) for lbl in rows[k]]
                for nid in child_nodes:
                    style_primary(nid)
                for nid in child_nodes:
                    out.append(f"    {root} --> {nid}")
                last_nodes = child_nodes
                k += 1
                if k < len(rows) and isinstance(rows[k], list):
                    row2_nodes = [_add_node(out, counter, lbl) for lbl in rows[k]]
                    for nid in row2_nodes:
                        style_secondary(nid)
                    if len(child_nodes) == len(row2_nodes):
                        for parent, child in zip(child_nodes, row2_nodes):
                            out.append(f"    {parent} --> {child}")
                    else:
                        anchor = child_nodes[len(child_nodes) // 2]
                        for nid in row2_nodes:
                            out.append(f"    {anchor} --> {nid}")
                    last_nodes = row2_nodes
                    k += 1
            else:
                last_nodes = [root]
            i = k
            continue

        i += 1

    return "\n".join(out) + "\n"


def text_diagram_to_mermaid(text: str, title: str = "") -> str:
    return rows_to_mermaid(parse_diagram_rows(text), title)
