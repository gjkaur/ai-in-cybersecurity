"""Lab 1.1 diagram generator — design system, layout validation, SVG output."""
from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from pathlib import Path

OUT = Path(__file__).resolve().parent
FONT = "Arial, Helvetica, sans-serif"
MONO = "Consolas, monospace"

C = {
    "bg": "#F8FAFC",
    "panel": "#FFFFFF",
    "border": "#E2E8F0",
    "text": "#0F172A",
    "muted": "#64748B",
    "blue": "#2563EB",
    "blue_bg": "#EFF6FF",
    "blue_border": "#93C5FD",
    "green": "#16A34A",
    "green_bg": "#ECFDF5",
    "green_border": "#86EFAC",
    "amber": "#D97706",
    "amber_bg": "#FFFBEB",
    "amber_border": "#FCD34D",
    "red": "#DC2626",
    "red_bg": "#FEE2E2",
    "red_border": "#FCA5A5",
    "orange": "#EA580C",
    "aws": "#FF9900",
    "aws_dark": "#C2410C",
    "slate": "#475569",
    "purple": "#7C3AED",
}

PHASE_COLORS = ["blue", "green", "amber", "red"]


def esc(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def svg(view: str, inner: str) -> str:
    w, h = view.split()[2], view.split()[3]
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view}" role="img">
  <defs>
    <filter id="sh" x="-15%" y="-15%" width="130%" height="130%">
      <feDropShadow dx="0" dy="2" stdDeviation="2.5" flood-color="#0F172A" flood-opacity="0.08"/>
    </filter>
    <linearGradient id="aws" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF9900"/><stop offset="100%" stop-color="#E65100"/>
    </linearGradient>
    {markers()}
  </defs>
  <rect width="{w}" height="{h}" fill="{C['bg']}"/>
{inner}
</svg>"""


def markers() -> str:
    parts = []
    for mid, color in [
        ("m-blue", C["blue"]),
        ("m-green", C["green"]),
        ("m-slate", C["slate"]),
        ("m-amber", C["amber"]),
        ("m-red", C["red"]),
    ]:
        parts.append(
            f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="7" markerHeight="7" orient="auto">'
            f'<path d="M1 2 L9 5 L1 8" fill="none" stroke="{color}" '
            f'stroke-width="1.8" stroke-linecap="round"/></marker>'
        )
    return "\n    ".join(parts)


def title(x: int, y: int, text: str, sub: str = "") -> str:
    s = (
        f'  <text x="{x}" y="{y}" text-anchor="middle" font-family="{FONT}" '
        f'font-size="20" font-weight="700" fill="{C["text"]}">{esc(text)}</text>\n'
    )
    if sub:
        s += (
            f'  <text x="{x}" y="{y + 20}" text-anchor="middle" font-family="{FONT}" '
            f'font-size="12" fill="{C["muted"]}">{esc(sub)}</text>\n'
        )
    return s


def panel(x: int, y: int, w: int, h: int, fill: str, stroke: str, rx: int = 12) -> str:
    return (
        f'  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="2" filter="url(#sh)"/>\n'
    )


def badge(x: int, y: int, n: str, color: str) -> str:
    return f"""  <circle cx="{x}" cy="{y}" r="14" fill="{color}"/>
  <text x="{x}" y="{y + 5}" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">{esc(n)}</text>
"""


def arrow(d: str, color: str, mid: str = "m-slate", width: float = 2.5) -> str:
    return (
        f'  <path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
        f'marker-end="url(#{mid})"/>\n'
    )


def tag(x: int, y: int, text: str, color: str) -> str:
    w = max(len(text) * 6 + 18, 36)
    return f"""  <rect x="{x - w // 2}" y="{y - 10}" width="{w}" height="20" rx="10" fill="#FFF" stroke="{color}" stroke-width="1"/>
  <text x="{x}" y="{y + 4}" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="{color}">{esc(text)}</text>
"""


def t(
    x: int,
    y: int,
    text: str,
    size: int = 12,
    weight: str = "400",
    color: str | None = None,
    anchor: str = "middle",
    family: str | None = None,
) -> str:
    fam = family or FONT
    col = color or C["text"]
    return (
        f'  <text x="{x}" y="{y}" text-anchor="{anchor}" font-family="{fam}" '
        f'font-size="{size}" font-weight="{weight}" fill="{col}">{esc(text)}</text>\n'
    )


def cmd_pill(x: int, y: int, w: int, text: str, color: str) -> str:
    return (
        f'  <rect x="{x}" y="{y}" width="{w}" height="22" rx="5" fill="#FFF" stroke="{color}"/>\n'
        + t(x + w // 2, y + 15, text, 9, "600", color, family=MONO)
    )


def icon_pc(x: int, y: int) -> str:
    return f"""  <rect x="{x}" y="{y}" width="40" height="30" rx="4" fill="{C['blue']}" opacity="0.15"/>
  <rect x="{x + 6}" y="{y + 4}" width="28" height="18" rx="2" fill="{C['blue']}" opacity="0.35"/>
  <rect x="{x + 14}" y="{y + 26}" width="12" height="3" rx="1" fill="{C['blue']}" opacity="0.5"/>
"""


def icon_server(x: int, y: int) -> str:
    return f"""  <rect x="{x}" y="{y}" width="36" height="34" rx="4" fill="{C['aws']}" opacity="0.2"/>
  <rect x="{x + 4}" y="{y + 5}" width="28" height="6" rx="2" fill="{C['aws']}" opacity="0.5"/>
  <rect x="{x + 4}" y="{y + 14}" width="28" height="6" rx="2" fill="{C['aws']}" opacity="0.5"/>
  <rect x="{x + 4}" y="{y + 23}" width="28" height="6" rx="2" fill="{C['aws']}" opacity="0.5"/>
"""


def icon_cloud(x: int, y: int) -> str:
    return f"""  <ellipse cx="{x + 18}" cy="{y + 14}" rx="16" ry="10" fill="{C['blue']}" opacity="0.15"/>
  <ellipse cx="{x + 10}" cy="{y + 16}" rx="8" ry="6" fill="{C['blue']}" opacity="0.25"/>
  <ellipse cx="{x + 26}" cy="{y + 16}" rx="8" ry="6" fill="{C['blue']}" opacity="0.25"/>
"""


def icon_lock(x: int, y: int, color: str) -> str:
    return f"""  <rect x="{x}" y="{y + 8}" width="16" height="12" rx="2" fill="none" stroke="{color}" stroke-width="1.5"/>
  <path d="M{x + 3} {y + 8} V{y + 4} a5 5 0 0 1 10 0 v4" fill="none" stroke="{color}" stroke-width="1.5"/>
"""


def icon_key(x: int, y: int, color: str) -> str:
    return f"""  <circle cx="{x + 6}" cy="{y + 6}" r="5" fill="none" stroke="{color}" stroke-width="1.5"/>
  <line x1="{x + 10}" y1="{y + 10}" x2="{x + 18}" y2="{y + 18}" stroke="{color}" stroke-width="1.5"/>
  <line x1="{x + 14}" y1="{y + 14}" x2="{x + 16}" y2="{y + 12}" stroke="{color}" stroke-width="1.5"/>
  <line x1="{x + 16}" y1="{y + 16}" x2="{x + 18}" y2="{y + 14}" stroke="{color}" stroke-width="1.5"/>
"""


def diagram_01_architecture() -> str:
    w, h = 960, 440
    inner = title(480, 40, "Lab Architecture", "Your PC connects to EC2 over SSH and HTTP")
    inner += panel(24, 64, 912, 352, C["panel"], C["border"], 14)

    inner += f'  <rect x="48" y="96" width="864" height="44" rx="10" fill="{C["blue_bg"]}" stroke="{C["blue_border"]}"/>\n'
    inner += icon_cloud(58, 102)
    inner += t(480, 124, "Internet", 13, "600", C["blue"])

    # Arrows behind cards — separate lanes for SSH and HTTP
    inner += arrow("M268 200 H340", C["blue"], "m-blue")
    inner += arrow("M268 290 H520", C["green"], "m-green")
    inner += tag(304, 186, "SSH :22", C["blue"])
    inner += tag(394, 276, "HTTP :80", C["green"])

    inner += panel(48, 156, 220, 220, C["blue_bg"], C["blue"])
    inner += icon_pc(68, 172)
    inner += t(158, 198, "Your PC", 14, "700", C["blue"])
    inner += t(158, 220, "VS Code + browser", 11, "400", C["muted"])
    inner += t(158, 240, "soc-lab-key.pem", 11, "400", C["muted"])
    inner += f'  <rect x="68" y="300" width="80" height="28" rx="6" fill="{C["blue"]}"/>\n'
    inner += t(108, 319, "SSH :22", 10, "700", "#FFF")
    inner += f'  <rect x="158" y="300" width="80" height="28" rx="6" fill="{C["green"]}"/>\n'
    inner += t(198, 319, "HTTP :80", 10, "700", "#FFF")

    inner += (
        f'  <rect x="300" y="148" width="612" height="236" rx="12" fill="#FAFAFA" '
        f'stroke="{C["slate"]}" stroke-width="2" stroke-dasharray="8 4"/>\n'
    )
    inner += t(320, 170, "AWS VPC", 12, "700", C["slate"], "start")

    inner += f'  <rect x="320" y="182" width="572" height="52" rx="8" fill="{C["amber_bg"]}" stroke="{C["amber_border"]}"/>\n'
    inner += t(340, 204, "Security Group", 12, "700", C["amber"], "start")
    inner += f'  <rect x="480" y="194" width="72" height="24" rx="5" fill="{C["red"]}"/>\n'
    inner += t(516, 210, "ALLOW :22", 9, "700", "#FFF")
    inner += f'  <rect x="562" y="194" width="72" height="24" rx="5" fill="{C["red"]}"/>\n'
    inner += t(598, 210, "ALLOW :80", 9, "700", "#FFF")
    inner += t(660, 210, "deny all other ports", 10, "400", C["muted"], "start")

    inner += (
        f'  <rect x="320" y="246" width="572" height="120" rx="10" fill="url(#aws)" '
        f'stroke="{C["aws_dark"]}" stroke-width="2"/>\n'
    )
    inner += icon_server(336, 268)
    inner += t(390, 278, "EC2 Instance", 14, "700", "#FFF", "start")
    inner += t(390, 296, "Amazon Linux 2023 · t2.medium", 10, "400", "#FFF7ED", "start")

    inner += f'  <rect x="520" y="278" width="150" height="64" rx="8" fill="rgba(255,255,255,0.22)" stroke="#FFF"/>\n'
    inner += t(595, 304, "nginx", 12, "700", "#FFF")
    inner += t(595, 322, "listens on :80", 9, "400", "#FFF7ED")

    inner += f'  <rect x="690" y="278" width="180" height="64" rx="8" fill="rgba(255,255,255,0.22)" stroke="#FFF"/>\n'
    inner += t(780, 304, "access.log", 11, "700", "#FFF")
    inner += t(780, 322, "telemetry data", 9, "400", "#FFF7ED")

    inner += f'  <rect x="48" y="388" width="864" height="28" rx="6" fill="#F1F5F9" stroke="{C["border"]}"/>\n'
    inner += t(
        480,
        406,
        "Blue = SSH remote access  ·  Green = HTTP web traffic  ·  Orange = AWS resources",
        10,
        "400",
        C["muted"],
    )
    return svg(f"0 0 {w} {h}", inner)


def diagram_02_vpc() -> str:
    w, h = 960, 380
    inner = title(480, 36, "VPC and Security Group", "Firewall rules control traffic to your instance")

    inner += arrow("M156 190 H214", C["slate"], "m-slate")
    inner += tag(185, 176, "ingress", C["slate"])
    inner += arrow("M500 190 H548", C["green"], "m-green")
    inner += tag(524, 176, "allowed", C["green"])

    inner += panel(40, 130, 116, 88, C["blue_bg"], C["blue_border"])
    inner += icon_cloud(52, 142)
    inner += t(98, 168, "Internet", 12, "700", C["blue"])
    inner += t(98, 186, "incoming", 10, "400", C["muted"])

    inner += (
        f'  <rect x="214" y="110" width="706" height="220" rx="14" fill="{C["panel"]}" '
        f'stroke="{C["slate"]}" stroke-width="2" stroke-dasharray="8 4" filter="url(#sh)"/>\n'
    )
    inner += t(234, 134, "VPC  ·  Subnet", 12, "700", C["slate"], "start")

    inner += panel(240, 150, 280, 160, C["red_bg"], C["red_border"])
    inner += t(380, 178, "Security Group", 14, "700", C["red"])
    inner += t(380, 196, "Virtual firewall", 10, "400", C["muted"])
    inner += f'  <rect x="268" y="212" width="108" height="28" rx="6" fill="{C["red"]}"/>\n'
    inner += t(322, 230, "ALLOW :22", 10, "700", "#FFF")
    inner += f'  <rect x="384" y="212" width="108" height="28" rx="6" fill="{C["red"]}"/>\n'
    inner += t(438, 230, "ALLOW :80", 10, "700", "#FFF")
    inner += f'  <rect x="268" y="252" width="224" height="28" rx="6" fill="{C["slate"]}"/>\n'
    inner += t(380, 270, "implicit deny (all else blocked)", 10, "600", "#FFF")

    inner += panel(548, 160, 340, 140, C["green_bg"], C["green_border"])
    inner += icon_server(568, 176)
    inner += t(700, 200, "EC2 Instance", 14, "700", C["green"])
    inner += t(700, 220, "Amazon Linux 2023", 10, "400", C["muted"])
    inner += t(700, 268, "Only matching traffic reaches the server", 10, "400", C["muted"])

    inner += f'  <rect x="40" y="348" width="880" height="24" rx="6" fill="{C["blue_bg"]}" stroke="{C["blue_border"]}"/>\n'
    inner += t(
        480,
        364,
        "Think of the Security Group as a bouncer — only ports 22 and 80 get in",
        11,
        "400",
        C["blue"],
    )
    return svg(f"0 0 {w} {h}", inner)


def diagram_03_ssh() -> str:
    w, h = 960, 320
    inner = title(480, 36, "SSH Key Authentication", "Private key on your PC matches public key on the server")

    cy = 168
    inner += arrow(f"M278 {cy} H318", C["blue"], "m-blue")
    inner += arrow(f"M642 {cy} H682", C["blue"], "m-blue")
    inner += tag(480, cy - 22, "encrypted tunnel · port 22", C["blue"])

    inner += panel(48, 88, 230, 180, C["blue_bg"], C["blue"])
    inner += icon_key(72, 108, C["blue"])
    inner += t(163, 118, "Your PC", 14, "700", C["blue"])
    inner += f'  <rect x="72" y="132" width="182" height="44" rx="8" fill="#FFF" stroke="{C["blue_border"]}"/>\n'
    inner += t(163, 160, "soc-lab-key.pem", 11, "600")
    inner += t(163, 192, "Private key — keep secret", 10, "400", C["muted"])
    inner += t(163, 210, "Never share this file", 10, "600", C["red"])
    inner += t(163, 248, "VS Code Remote-SSH", 10, "400", C["muted"])

    inner += (
        f'  <rect x="318" y="118" width="324" height="120" rx="12" fill="#FFF" '
        f'stroke="{C["blue"]}" stroke-width="1.5" stroke-dasharray="6 4"/>\n'
    )
    inner += t(480, 148, "Challenge / response", 13, "600", C["blue"])
    inner += t(480, 172, "Server sends random data", 11, "400", C["muted"])
    inner += t(480, 192, "PC signs with private key", 11, "400", C["muted"])
    inner += t(480, 212, "Server verifies with public key", 11, "400", C["muted"])

    inner += panel(682, 88, 230, 180, C["green_bg"], C["green_border"])
    inner += icon_lock(706, 108, C["green"])
    inner += t(797, 118, "EC2 Server", 14, "700", C["green"])
    inner += f'  <rect x="706" y="132" width="182" height="44" rx="8" fill="#FFF" stroke="{C["green_border"]}"/>\n'
    inner += t(797, 160, "authorized_keys", 11, "600")
    inner += t(797, 192, "Public key from AWS", 10, "400", C["muted"])
    inner += t(797, 210, "Login: ec2-user", 10, "400", C["muted"])
    inner += t(797, 248, "No password needed", 10, "400", C["muted"])

    inner += f'  <rect x="48" y="284" width="864" height="28" rx="6" fill="#F1F5F9" stroke="{C["border"]}"/>\n'
    inner += t(480, 302, "If keys match → access granted. If not → connection refused.", 10, "400", C["muted"])
    return svg(f"0 0 {w} {h}", inner)


def diagram_04_chmod() -> str:
    w, h = 960, 340
    inner = title(480, 36, "chmod +x", "Make a script executable, then run it")

    cy = 178
    inner += arrow("M168 178 H196", C["slate"], "m-slate")
    inner += arrow("M336 178 H364", C["slate"], "m-slate")
    inner += arrow("M504 178 H532", C["slate"], "m-slate")
    inner += tag(182, 158, "chmod +x", C["blue"])
    inner += tag(350, 158, "./hello.sh", C["purple"])

    inner += badge(97, 126, "1", C["amber"])
    inner += panel(48, 138, 120, 88, "#FEF3C7", C["amber"])
    inner += t(108, 170, "hello.sh", 12, "700", C["amber"])
    inner += t(108, 190, "-rw-r--r--", 10, "400", C["amber"], family=MONO)
    inner += t(108, 210, "not executable", 9, "400", C["muted"])

    inner += badge(265, 126, "2", C["blue"])
    inner += panel(196, 138, 140, 88, C["green_bg"], C["green_border"])
    inner += t(266, 170, "hello.sh", 12, "700", C["green"])
    inner += t(266, 190, "-rwxr-xr-x", 10, "400", C["green"], family=MONO)
    inner += t(266, 210, "x = execute", 9, "400", C["muted"])

    inner += badge(433, 126, "3", C["purple"])
    inner += panel(364, 138, 140, 88, C["blue_bg"], C["blue_border"])
    inner += t(434, 178, "Hello SOC", 13, "700", C["blue"])
    inner += t(434, 198, "script runs", 9, "400", C["muted"])
    inner += t(434, 212, "in terminal", 9, "400", C["muted"])

    inner += panel(540, 118, 380, 130, C["panel"], C["border"])
    inner += t(730, 140, "Permission bits (rwx)", 12, "700")
    inner += t(570, 166, "r = read", 10, "400", C["muted"], "start")
    inner += t(570, 184, "w = write", 10, "400", C["muted"], "start")
    inner += t(570, 202, "x = execute", 10, "400", C["muted"], "start")
    inner += t(780, 176, "owner   group   other", 10, "400", C["muted"])
    inner += t(780, 196, "-rw-    r--     r-x", 10, "600", family=MONO)
    inner += t(730, 228, "chmod +x adds execute (x) for owner, group, and other", 10, "400", C["muted"])

    inner += cmd_pill(48, 268, 130, "chmod +x hello.sh", C["blue"])
    inner += cmd_pill(196, 268, 110, "./hello.sh", C["purple"])
    inner += f'  <rect x="48" y="302" width="864" height="28" rx="6" fill="#F1F5F9" stroke="{C["border"]}"/>\n'
    inner += t(480, 320, "Without +x the shell cannot run the file as a program", 10, "400", C["muted"])
    return svg(f"0 0 {w} {h}", inner)


def diagram_05_setuid() -> str:
    w, h = 960, 320
    inner = title(480, 36, "SetUID", "Program runs as file owner, not who launched it")

    cy = 168
    inner += arrow(f"M228 {cy} H262", C["slate"], "m-slate")
    inner += arrow(f"M482 {cy} H516", C["slate"], "m-slate")
    inner += tag(245, 148, "executes", C["slate"])
    inner += tag(499, 148, "runs as root", C["green"])

    inner += panel(48, 120, 180, 96, C["blue_bg"], C["blue_border"])
    inner += t(138, 152, "ec2-user", 13, "700", C["blue"])
    inner += t(138, 174, "normal user", 10, "400", C["muted"])
    inner += t(138, 192, "runs passwd", 10, "400", C["muted"])

    inner += panel(262, 120, 220, 96, C["red_bg"], C["red_border"])
    inner += t(372, 152, "/usr/bin/passwd", 12, "700", C["red"])
    inner += t(372, 174, "-rwsr-xr-x", 11, "600", C["red"], family=MONO)
    inner += t(372, 192, "s = SetUID bit", 10, "400", C["red"])

    inner += panel(516, 120, 180, 96, C["green_bg"], C["green_border"])
    inner += t(606, 152, "root", 13, "700", C["green"])
    inner += t(606, 174, "elevated privileges", 10, "400", C["muted"])
    inner += t(606, 192, "effective user", 10, "400", C["muted"])

    inner += f'  <rect x="48" y="232" width="864" height="56" rx="8" fill="#FEF3C7" stroke="{C["amber_border"]}"/>\n'
    inner += t(480, 252, "Defender: inventory SetUID binaries on every Linux host", 11, "600", C["amber"])
    inner += t(
        480,
        272,
        "find / -perm -4000 -exec ls -l {} \\; 2>/dev/null",
        9,
        "400",
        C["amber"],
        family=MONO,
    )
    return svg(f"0 0 {w} {h}", inner)


def diagram_06_nginx() -> str:
    w, h = 960, 340
    inner = title(480, 36, "HTTP Request to Telemetry", "Each web hit writes one line to access.log")

    cy = 178
    inner += arrow("M178 178 H208", C["slate"], "m-slate")
    inner += arrow("M328 178 H358", C["slate"], "m-slate")
    inner += arrow("M478 178 H508", C["slate"], "m-slate")

    steps = [
        (48, "1", C["blue"], C["blue_bg"], C["blue_border"], "Browser", "GET /"),
        (208, "2", C["amber"], C["amber_bg"], C["amber_border"], "nginx", "port 80"),
        (358, "3", C["slate"], "#F1F5F9", C["border"], "access.log", "1 line per hit"),
        (508, "4", C["green"], C["green_bg"], C["green_border"], "Lab 1.2+", "AI detection"),
    ]
    for x, num, col, bg, border, head, sub in steps:
        inner += badge(x + 60, 126, num, col)
        inner += panel(x, 138, 130, 88, bg, border)
        inner += t(x + 65, 172, head, 12, "700", col)
        inner += t(x + 65, 192, sub, 10, "400", C["muted"])

    inner += f'  <rect x="48" y="248" width="864" height="72" rx="10" fill="{C["panel"]}" stroke="{C["border"]}"/>\n'
    inner += t(480, 272, "Sample access.log line", 12, "600")
    inner += t(480, 296, '192.0.2.1 - - [16/Jun/2026:10:00:01 +0000] "GET / HTTP/1.1" 200 612', 9, "400", C["muted"], family=MONO)
    inner += t(480, 312, "IP · timestamp · request · status code · bytes sent", 9, "400", C["muted"])
    return svg(f"0 0 {w} {h}", inner)


def diagram_00_roadmap() -> str:
    phases = [
        ("Phase 1 · AWS Setup", "blue", [
            ("1", "Create SSH key", "soc-lab-key.pem"),
            ("2", "Launch EC2", "ports 22, 80"),
            ("3", "Get public IP", ""),
        ]),
        ("Phase 2 · Connect", "green", [
            ("4", "SSH config", "VS Code"),
            ("5", "Connect EC2", "Remote terminal"),
        ]),
        ("Phase 3 · Linux", "amber", [
            ("6", "Scripts & chmod", "hello.sh"),
            ("7", "SetUID find", "privilege risk"),
        ]),
        ("Phase 4 · Web", "red", [
            ("8", "nginx + access.log", "Lab 1.2 telemetry"),
        ]),
    ]

    phase_h = 118
    gap = 26
    card_h = 58
    card_w = 190
    card_gap = 28
    inner_w = 720
    start_y = 138
    panel_top = 68

    # Compute total canvas height
    n_phases = len(phases)
    content_h = start_y + n_phases * phase_h + (n_phases - 1) * gap + 80
    h = content_h + 40
    w = 800

    inner = title(400, 44, "Lab 1.1 Roadmap", "8 steps · us-east-1 · personal AWS")
    inner += panel(20, panel_top, 760, content_h - panel_top + 20, C["panel"], C["border"], 14)
    inner += f'  <circle cx="400" cy="98" r="22" fill="{C["green"]}"/>\n'
    inner += t(400, 104, "START", 12, "700", "#FFF")
    inner += arrow(f"M400 120 V{start_y - 8}", C["slate"], "m-slate")

    y = start_y
    for i, (label, color_key, steps) in enumerate(phases):
        bg = C[f"{color_key}_bg"]
        border = C[color_key]
        accent = C[color_key]
        marker = f"m-{color_key}"

        inner += (
            f'  <rect x="40" y="{y}" width="{inner_w}" height="{phase_h}" rx="10" '
            f'fill="{bg}" stroke="{border}" stroke-width="2"/>\n'
        )
        inner += t(58, y + 24, label, 13, "700", accent, "start")

        n = len(steps)
        total = n * card_w + (n - 1) * card_gap
        start_x = 40 + (inner_w - total) // 2
        cy = y + 36 + card_h // 2

        for j, (num, title_txt, sub) in enumerate(steps):
            cx = start_x + j * (card_w + card_gap)
            inner += (
                f'  <rect x="{cx}" y="{y + 36}" width="{card_w}" height="{card_h}" '
                f'rx="8" fill="#FFF" stroke="{border}"/>\n'
            )
            inner += badge(cx + 22, y + 58, num, accent)
            inner += t(cx + card_w // 2 + 10, y + 62, title_txt, 11, "600", accent)
            if sub:
                inner += t(cx + card_w // 2 + 10, y + 78, sub, 9, "400", C["muted"])
            if j < n - 1:
                inner += arrow(
                    f"M{cx + card_w} {cy} H{cx + card_w + card_gap}",
                    accent,
                    marker,
                )

        if i < n_phases - 1:
            next_y = y + phase_h + gap
            inner += arrow(f"M400 {y + phase_h} V{next_y - 6}", C["slate"], "m-slate")
        y += phase_h + gap

    done_y = y + 8
    inner += f'  <rect x="320" y="{done_y}" width="160" height="44" rx="22" fill="{C["green"]}"/>\n'
    inner += t(400, done_y + 28, "Done", 14, "700", "#FFF")
    return svg(f"0 0 {w} {h}", inner)


def validate_all() -> list[str]:
    errors: list[str] = []
    hex_re = re.compile(r'(?:fill|stroke)="(#[0-9A-Fa-f]{3,8})"')
    for path in sorted(OUT.glob("*.svg")):
        text = path.read_text(encoding="utf-8")
        try:
            ET.fromstring(text)
        except ET.ParseError as exc:
            errors.append(f"{path.name}: invalid XML — {exc}")
        for m in hex_re.finditer(text):
            if not re.fullmatch(r"#[0-9A-Fa-f]{3,8}", m.group(1)):
                errors.append(f"{path.name}: bad color {m.group(1)}")
        if "FFGapic" in text or "%call" in text:
            errors.append(f"{path.name}: corrupted content")
        if text.count("<svg") != 1:
            errors.append(f"{path.name}: expected one svg root")
    return errors


DIAGRAMS = {
    "01-architecture.svg": diagram_01_architecture,
    "02-vpc-networking.svg": diagram_02_vpc,
    "03-ssh-keys.svg": diagram_03_ssh,
    "04-chmod-flow.svg": diagram_04_chmod,
    "05-setuid-flow.svg": diagram_05_setuid,
    "06-nginx-telemetry.svg": diagram_06_nginx,
    "00-complete-roadmap.svg": diagram_00_roadmap,
}


def main() -> None:
    for name, fn in DIAGRAMS.items():
        content = fn()
        (OUT / name).write_text(content.strip() + "\n", encoding="utf-8")
        print(f"  wrote {name}")

    issues = validate_all()
    if issues:
        print("VALIDATION FAILED:")
        for issue in issues:
            print(f"  - {issue}")
        raise SystemExit(1)
    print("All 7 diagrams passed validation")


if __name__ == "__main__":
    main()
