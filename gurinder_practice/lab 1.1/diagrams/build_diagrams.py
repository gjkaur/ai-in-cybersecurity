"""Regenerate lab 1.1 SVG diagrams — clean layout, clear arrows."""
from pathlib import Path

OUT = Path(__file__).resolve().parent
FONT = "Arial, Helvetica, Sans-serif"


def write(name: str, content: str) -> None:
    (OUT / name).write_text(content.strip() + "\n", encoding="utf-8")


def arrow(id_: str, color: str) -> str:
    return (
        f'<marker id="{id_}" viewBox="0 0 10 10" refX="9" refY="5" '
        f'markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M1 1 L9 5 L1 9" fill="none" stroke="{color}" '
        f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></marker>'
    )


def hline(x1, y1, x2, y2, color, marker_id, width=2.5):
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
        f'stroke="{color}" stroke-width="{width}" marker-end="url(#{marker_id})"/>'
    )


def vline(x1, y1, x2, y2, color, marker_id, width=2.5):
    return hline(x1, y1, x2, y2, color, marker_id, width)


A = arrow("a", "#475569")
B = arrow("b", "#2563EB")
G = arrow("g", "#16A34A")
O = arrow("o", "#D97706")
R = arrow("r", "#DC2626")


write("00-complete-roadmap.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 820" role="img" aria-label="Lab 1.1 step roadmap">
  <defs>{A}{B}{G}{O}{R}</defs>
  <rect width="760" height="820" fill="#F8FAFC"/>

  <text x="380" y="40" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="700" fill="#0F172A">Lab 1.1 Roadmap</text>
  <text x="380" y="62" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#64748B">8 steps · us-east-1</text>

  <circle cx="380" cy="92" r="22" fill="#16A34A"/>
  <text x="380" y="98" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">GO</text>
  {vline(380, 114, 380, 132, "#475569", "a")}

  <!-- Phase 1 -->
  <rect x="30" y="132" width="700" height="118" rx="10" fill="#EFF6FF" stroke="#2563EB" stroke-width="1.5"/>
  <text x="48" y="156" font-family="{FONT}" font-size="13" font-weight="700" fill="#1E40AF">Phase 1 · AWS Setup</text>
  <g>
    <rect x="60" y="168" width="190" height="58" rx="8" fill="#FFF" stroke="#2563EB"/>
    <circle cx="82" cy="197" r="14" fill="#2563EB"/><text x="82" y="202" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">1</text>
    <text x="165" y="194" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#1E3A8A">Create SSH key</text>
    <text x="165" y="212" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">soc-lab-key.pem</text>
  </g>
  {hline(250, 197, 278, 197, "#2563EB", "b")}
  <g>
    <rect x="278" y="168" width="190" height="58" rx="8" fill="#FFF" stroke="#2563EB"/>
    <circle cx="300" cy="197" r="14" fill="#2563EB"/><text x="300" y="202" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">2</text>
    <text x="383" y="194" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#1E3A8A">Launch EC2</text>
    <text x="383" y="212" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">ports 22, 80</text>
  </g>
  {hline(468, 197, 496, 197, "#2563EB", "b")}
  <g>
    <rect x="496" y="168" width="190" height="58" rx="8" fill="#FFF" stroke="#2563EB"/>
    <circle cx="518" cy="197" r="14" fill="#2563EB"/><text x="518" y="202" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">3</text>
    <text x="601" y="203" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#1E3A8A">Get public IP</text>
  </g>
  {vline(380, 250, 380, 268, "#475569", "a")}

  <!-- Phase 2 -->
  <rect x="30" y="268" width="700" height="118" rx="10" fill="#ECFDF5" stroke="#16A34A" stroke-width="1.5"/>
  <text x="48" y="292" font-family="{FONT}" font-size="13" font-weight="700" fill="#166534">Phase 2 · Connect</text>
  <g>
    <rect x="195" y="304" width="190" height="58" rx="8" fill="#FFF" stroke="#16A34A"/>
    <circle cx="217" cy="333" r="14" fill="#16A34A"/><text x="217" y="338" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">4</text>
    <text x="300" y="339" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#166534">SSH config</text>
  </g>
  {hline(385, 333, 413, 333, "#16A34A", "g")}
  <g>
    <rect x="413" y="304" width="190" height="58" rx="8" fill="#FFF" stroke="#16A34A"/>
    <circle cx="435" cy="333" r="14" fill="#16A34A"/><text x="435" y="338" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">5</text>
    <text x="518" y="339" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#166534">Connect EC2</text>
  </g>
  {vline(380, 386, 380, 404, "#475569", "a")}

  <!-- Phase 3 -->
  <rect x="30" y="404" width="700" height="118" rx="10" fill="#fffbeb" stroke="#D97706" stroke-width="1.5"/>
  <text x="48" y="428" font-family="{FONT}" font-size="13" font-weight="700" fill="#92400E">Phase 3 · Linux</text>
  <g>
    <rect x="195" y="440" width="190" height="58" rx="8" fill="#FFF" stroke="#D97706"/>
    <circle cx="217" cy="469" r="14" fill="#D97706"/><text x="217" y="474" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">6</text>
    <text x="300" y="475" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#92400E">Scripts &amp; chmod</text>
  </g>
  {hline(385, 469, 413, 469, "#D97706", "o")}
  <g>
    <rect x="413" y="440" width="190" height="58" rx="8" fill="#FFF" stroke="#D97706"/>
    <circle cx="435" cy="469" r="14" fill="#D97706"/><text x="435" y="474" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">7</text>
    <text x="518" y="475" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#92400E">SetUID find</text>
  </g>
  {vline(380, 522, 380, 540, "#475569", "a")}

  <!-- Phase 4 -->
  <rect x="30" y="540" width="700" height="118" rx="10" fill="#FEE2E2" stroke="#DC2626" stroke-width="1.5"/>
  <text x="48" y="564" font-family="{FONT}" font-size="13" font-weight="700" fill="#991B1B">Phase 4 · Web</text>
  <g>
    <rect x="285" y="576" width="190" height="58" rx="8" fill="#FFF" stroke="#DC2626"/>
    <circle cx="307" cy="605" r="14" fill="#DC2626"/><text x="307" y="610" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="700" fill="#FFF">8</text>
    <text x="390" y="611" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#991B1B">nginx + access.log</text>
  </g>
  {vline(380, 658, 380, 676, "#16A34A", "g")}

  <rect x="300" y="676" width="160" height="44" rx="22" fill="#16A34A"/>
  <text x="380" y="704" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#FFF">Done</text>
</svg>
""")


write("01-architecture.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 460" role="img" aria-label="Lab 1.1 architecture">
  <defs>
    {B}{G}
    <linearGradient id="aws" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#FF9900"/><stop offset="100%" stop-color="#E65100"/>
    </linearGradient>
  </defs>
  <rect width="820" height="460" fill="#F8FAFC"/>
  <text x="410" y="36" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="#0F172A">Lab Architecture</text>

  <rect x="40" y="56" width="740" height="32" rx="6" fill="#E0F2FE" stroke="#0284C7"/>
  <text x="410" y="77" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#0369A1">Internet</text>

  <!-- PC -->
  <rect x="40" y="108" width="180" height="160" rx="10" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
  <text x="130" y="136" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#1E40AF">Your PC</text>
  <text x="130" y="158" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#475569">VS Code + browser</text>
  <text x="130" y="176" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#475569">soc-lab-key.pem</text>
  <rect x="58" y="196" width="68" height="24" rx="5" fill="#2563EB"/>
  <text x="92" y="212" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#FFF">:22</text>
  <rect x="134" y="196" width="68" height="24" rx="5" fill="#16A34A"/>
  <text x="168" y="212" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#FFF">:80</text>

  <!-- VPC -->
  <rect x="250" y="108" width="530" height="320" rx="10" fill="#FAFAFA" stroke="#94A3B8" stroke-width="1.5" stroke-dasharray="5 3"/>
  <text x="268" y="130" font-family="{FONT}" font-size="11" font-weight="700" fill="#64748B">VPC</text>

  <rect x="270" y="144" width="490" height="248" rx="8" fill="#FFF7ED" stroke="#F59E0B" stroke-width="1.5"/>
  <text x="290" y="164" font-family="{FONT}" font-size="12" font-weight="700" fill="#92400E">Security Group</text>
  <rect x="290" y="174" width="72" height="22" rx="4" fill="#DC2626"/>
  <text x="326" y="189" text-anchor="middle" font-family="{FONT}" font-size="9" font-weight="600" fill="#FFF">:22</text>
  <rect x="370" y="174" width="72" height="22" rx="4" fill="#DC2626"/>
  <text x="406" y="189" text-anchor="middle" font-family="{FONT}" font-size="9" font-weight="600" fill="#FFF">:80</text>

  <rect x="290" y="210" width="450" height="130" rx="10" fill="url(#aws)" stroke="#C2410C" stroke-width="2"/>
  <text x="515" y="240" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="700" fill="#FFF">EC2</text>
  <text x="515" y="260" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#FFF7ED">Amazon Linux · t2.medium</text>
  <rect x="310" y="276" width="120" height="48" rx="6" fill="rgba(255,255,255,0.22)" stroke="#FFF"/>
  <text x="575" y="305" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#FFF">nginx :80</text>
  <rect x="620" y="276" width="100" height="48" rx="6" fill="rgba(255,255,255,0.22)" stroke="#FFF"/>
  <text x="670" y="305" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#FFF">access.log</text>

  <!-- Arrows PC to EC2 -->
  <path d="M220 208 C240 208 255 248 270 248" fill="none" stroke="#2563EB" stroke-width="2.5" marker-end="url(#b)"/>
  <text x="228" y="222" font-family="{FONT}" font-size="10" font-weight="600" fill="#2563EB">SSH</text>
  <path d="M220 220 C240 220 255 290 290 290" fill="none" stroke="#16A34A" stroke-width="2.5" marker-end="url(#g)"/>
  <text x="228" y="248" font-family="{FONT}" font-size="10" font-weight="600" fill="#16A34A">HTTP</text>

  <rect x="40" y="420" width="740" height="28" rx="6" fill="#F1F5F9"/>
  <text x="410" y="439" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Blue = SSH · Green = HTTP · Orange = AWS</text>
</svg>
""")


write("02-vpc-networking.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 320" role="img" aria-label="VPC networking">
  <defs>{A}</defs>
  <rect width="760" height="320" fill="#F8FAFC"/>
  <text x="380" y="36" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="#0F172A">VPC &amp; Security Group</text>
  <text x="380" y="56" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">Firewall rules control what reaches your instance</text>

  <rect x="40" y="80" width="680" height="200" rx="12" fill="#FFF" stroke="#94A3B8" stroke-width="1.5"/>
  <text x="380" y="104" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#64748B">Subnet</text>

  <rect x="70" y="120" width="280" height="140" rx="10" fill="#FEE2E2" stroke="#DC2626" stroke-width="2"/>
  <text x="210" y="148" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#991B1B">Security Group</text>
  <rect x="100" y="162" width="100" height="26" rx="5" fill="#DC2626"/>
  <text x="150" y="180" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#FFF">ALLOW :22</text>
  <rect x="210" y="162" width="100" height="26" rx="5" fill="#DC2626"/>
  <text x="260" y="180" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#FFF">ALLOW :80</text>
  <rect x="100" y="198" width="210" height="26" rx="5" fill="#64748B"/>
  <text x="205" y="216" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#FFF">DENY everything else</text>

  <rect x="410" y="140" width="280" height="100" rx="10" fill="#DCFCE7" stroke="#16A34A" stroke-width="2"/>
  <text x="550" y="178" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#166534">EC2 Instance</text>
  <text x="550" y="200" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#15803D">Only matching traffic passes</text>

  {hline(350, 190, 405, 190, "#334155", "a", 3)}
  <text x="378" y="182" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#334155">ingress</text>
</svg>
""")


write("03-ssh-keys.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 260" role="img" aria-label="SSH key authentication">
  <defs>{B}</defs>
  <rect width="760" height="260" fill="#F8FAFC"/>
  <text x="380" y="36" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="#0F172A">SSH Key Authentication</text>

  <rect x="40" y="72" width="220" height="140" rx="10" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
  <text x="150" y="100" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#1E40AF">Your PC</text>
  <rect x="68" y="116" width="164" height="44" rx="6" fill="#FFF" stroke="#93C5FD"/>
  <text x="150" y="144" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#334155">soc-lab-key.pem</text>
  <text x="150" y="176" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Private key — keep secret</text>

  <rect x="500" y="72" width="220" height="140" rx="10" fill="#DCFCE7" stroke="#16A34A" stroke-width="2"/>
  <text x="610" y="100" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#166534">EC2</text>
  <rect x="528" y="116" width="164" height="44" rx="6" fill="#FFF" stroke="#86EFAC"/>
  <text x="610" y="144" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#334155">authorized_keys</text>
  <text x="610" y="176" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Login: ec2-user</text>

  {hline(260, 142, 500, 142, "#2563EB", "b", 3)}
  <text x="380" y="132" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#2563EB">Encrypted · port 22</text>
</svg>
""")


write("04-chmod-flow.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 220" role="img" aria-label="chmod permission flow">
  <defs>{A}</defs>
  <rect width="780" height="220" fill="#F8FAFC"/>
  <text x="390" y="32" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="#0F172A">chmod +x</text>
  <text x="390" y="52" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">Make a script executable, then run it</text>

  <rect x="40" y="88" width="90" height="64" rx="8" fill="#FEF3C7" stroke="#F59E0B" stroke-width="2"/>
  <text x="85" y="114" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#92400E">hello.sh</text>
  <text x="85" y="132" text-anchor="middle" font-family="monospace" font-size="10" fill="#78350F">-rw-r--r--</text>

  {hline(130, 120, 158, 120, "#475569", "a")}
  <text x="144" y="112" text-anchor="middle" font-family="monospace" font-size="11" fill="#2563EB">chmod +x</text>

  <rect x="158" y="88" width="90" height="64" rx="8" fill="#DCFCE7" stroke="#22C55E" stroke-width="2"/>
  <text x="203" y="114" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#166534">hello.sh</text>
  <text x="203" y="132" text-anchor="middle" font-family="monospace" font-size="10" fill="#15803D">-rwxr-xr-x</text>

  {hline(248, 120, 276, 120, "#475569", "a")}
  <text x="262" y="112" text-anchor="middle" font-family="monospace" font-size="11" fill="#7C3AED">./hello.sh</text>

  <rect x="276" y="88" width="90" height="64" rx="8" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
  <text x="321" y="122" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#1E40AF">Hello SOC</text>

  <rect x="420" y="88" width="320" height="64" rx="8" fill="#FFF" stroke="#E2E8F0"/>
  <text x="440" y="112" font-family="{FONT}" font-size="11" fill="#64748B">r = read</text>
  <text x="440" y="132" font-family="{FONT}" font-size="11" fill="#64748B">w = write</text>
  <text x="530" y="112" font-family="{FONT}" font-size="11" fill="#64748B">x = execute</text>
  <text x="530" y="132" font-family="{FONT}" font-size="11" fill="#64748B">+x adds run permission</text>
</svg>
""")


write("05-setuid-flow.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 240" role="img" aria-label="SetUID privilege flow">
  <defs>{A}</defs>
  <rect width="780" height="240" fill="#F8FAFC"/>
  <text x="390" y="32" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="#0F172A">SetUID</text>
  <text x="390" y="52" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">Runs as file owner, not who launched it</text>

  <rect x="50" y="80" width="170" height="90" rx="10" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
  <text x="135" y="112" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="600" fill="#1E40AF">ec2-user</text>
  <text x="135" y="134" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">runs passwd</text>

  {hline(220, 125, 268, 125, "#475569", "a", 3)}

  <rect x="268" y="80" width="200" height="90" rx="10" fill="#FEE2E2" stroke="#EF4444" stroke-width="2"/>
  <text x="368" y="112" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#991B1B">/usr/bin/passwd</text>
  <text x="368" y="134" text-anchor="middle" font-family="monospace" font-size="11" fill="#7F1D1D">-rwsr-xr-x</text>
  <text x="368" y="154" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#7F1D1D">s = SetUID bit</text>

  {hline(468, 125, 516, 125, "#475569", "a", 3)}

  <rect x="516" y="80" width="170" height="90" rx="10" fill="#DCFCE7" stroke="#16A34A" stroke-width="2"/>
  <text x="601" y="112" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="600" fill="#166534">root</text>
  <text x="601" y="134" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">elevated run</text>

  <rect x="50" y="188" width="680" height="36" rx="8" fill="#FEF3C7" stroke="#F59E0B"/>
  <text x="390" y="210" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#92400E">Defenders: find SetUID binaries with find / -perm -4000</text>
</svg>
""")


write("06-nginx-telemetry.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 760 220" role="img" aria-label="nginx telemetry flow">
  <defs>{A}</defs>
  <rect width="760" height="220" fill="#F8FAFC"/>
  <text x="380" y="32" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="#0F172A">Request to Log</text>
  <text x="380" y="52" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">Each HTTP hit writes one line to access.log</text>

  <rect x="40" y="88" width="120" height="64" rx="8" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
  <text x="100" y="114" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#1E40AF">Browser</text>
  <text x="100" y="132" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">GET /</text>

  {hline(160, 120, 198, 120, "#475569", "a", 3)}

  <rect x="198" y="88" width="120" height="64" rx="8" fill="#FFF7ED" stroke="#F59E0B" stroke-width="2"/>
  <text x="258" y="114" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#92400E">nginx</text>
  <text x="258" y="132" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#78350F">:80</text>

  {hline(318, 120, 356, 120, "#475569", "a", 3)}

  <rect x="356" y="88" width="140" height="64" rx="8" fill="#F1F5F9" stroke="#64748B" stroke-width="2"/>
  <text x="426" y="114" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#334155">access.log</text>
  <text x="426" y="132" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">1 line / hit</text>

  {hline(496, 120, 534, 120, "#475569", "a", 3)}

  <rect x="534" y="88" width="140" height="64" rx="8" fill="#DCFCE7" stroke="#22C55E" stroke-width="2"/>
  <text x="604" y="114" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#166534">Lab 1.2+</text>
  <text x="604" y="132" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#15803D">AI detection</text>
</svg>
""")

print("Wrote 7 clean diagrams")
