"""Regenerate lab 1.1 SVG diagrams with improved readability."""
from pathlib import Path

OUT = Path(__file__).resolve().parent
FONT = "Arial, Helvetica, Sans-serif"

def write(name: str, content: str) -> None:
    (OUT / name).write_text(content.strip() + "\n", encoding="utf-8")


write("00-complete-roadmap.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 920" role="img" aria-label="Lab 1.1 complete step roadmap">
  <defs>
    <marker id="a" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8Z" fill="#475569"/></marker>
  </defs>
  <rect width="800" height="920" fill="#F1F5F9"/>
  <rect x="16" y="16" width="768" height="888" rx="16" fill="#FFFFFF" stroke="#CBD5E1" stroke-width="2"/>

  <rect x="32" y="32" width="736" height="56" rx="12" fill="#0F172A"/>
  <text x="400" y="58" text-anchor="middle" font-family="{FONT}" font-size="20" font-weight="700" fill="#FFFFFF">Lab 1.1 Complete Roadmap</text>
  <text x="400" y="78" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#94A3B8">8 steps · 4 phases · personal AWS · us-east-1</text>

  <circle cx="400" cy="118" r="24" fill="#16A34A"/>
  <text x="400" y="124" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="700" fill="#FFFFFF">START</text>
  <line x1="400" y1="142" x2="400" y2="158" stroke="#475569" stroke-width="2" marker-end="url(#a)"/>

  <!-- Phase 1 -->
  <rect x="40" y="162" width="720" height="148" rx="12" fill="#EFF6FF" stroke="#2563EB" stroke-width="2"/>
  <text x="56" y="188" font-family="{FONT}" font-size="14" font-weight="700" fill="#1E40AF">Phase 1 — AWS Setup</text>
  <text x="56" y="206" font-family="{FONT}" font-size="11" fill="#64748B">Steps 1–3 · CloudShell · ~20 min</text>
  <g>
    <rect x="70" y="220" width="200" height="72" rx="10" fill="#FFFFFF" stroke="#2563EB"/>
    <circle cx="92" cy="244" r="16" fill="#2563EB"/><text x="92" y="249" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#FFF">1</text>
    <text x="175" y="242" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#1E3A8A">Create SSH Key</text>
    <text x="175" y="260" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">soc-lab-key.pem</text>
    <text x="175" y="276" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Download to PC</text>
  </g>
  <line x1="270" y1="256" x2="300" y2="256" stroke="#2563EB" stroke-width="2" marker-end="url(#a)"/>
  <g>
    <rect x="300" y="220" width="200" height="72" rx="10" fill="#FFFFFF" stroke="#2563EB"/>
    <circle cx="322" cy="244" r="16" fill="#2563EB"/><text x="322" y="249" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#FFF">2</text>
    <text x="405" y="242" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#1E3A8A">Launch EC2</text>
    <text x="405" y="260" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Security group</text>
    <text x="405" y="276" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">ports 22 + 80</text>
  </g>
  <line x1="500" y1="256" x2="530" y2="256" stroke="#2563EB" stroke-width="2" marker-end="url(#a)"/>
  <g>
    <rect x="530" y="220" width="200" height="72" rx="10" fill="#FFFFFF" stroke="#2563EB"/>
    <circle cx="552" cy="244" r="16" fill="#2563EB"/><text x="552" y="249" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#FFF">3</text>
    <text x="635" y="242" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#1E3A8A">Get Public IP</text>
    <text x="635" y="260" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Record in worksheet</text>
  </g>
  <line x1="400" y1="310" x2="400" y2="330" stroke="#475569" stroke-width="2" marker-end="url(#a)"/>

  <!-- Phase 2 -->
  <rect x="40" y="330" width="720" height="148" rx="12" fill="#ECFDF5" stroke="#16A34A" stroke-width="2"/>
  <text x="56" y="356" font-family="{FONT}" font-size="14" font-weight="700" fill="#166534">Phase 2 — Connect (VS Code)</text>
  <text x="56" y="374" font-family="{FONT}" font-size="11" fill="#64748B">Steps 4–5 · Your Windows PC · ~10 min</text>
  <g>
    <rect x="180" y="388" width="200" height="72" rx="10" fill="#FFFFFF" stroke="#16A34A"/>
    <circle cx="202" cy="412" r="16" fill="#16A34A"/><text x="202" y="417" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#FFF">4</text>
    <text x="285" y="410" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#166534">SSH Config</text>
    <text x="285" y="428" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Host + IdentityFile</text>
  </g>
  <line x1="380" y1="412" x2="410" y2="412" stroke="#16A34A" stroke-width="2" marker-end="url(#a)"/>
  <g>
    <rect x="410" y="388" width="200" height="72" rx="10" fill="#FFFFFF" stroke="#16A34A"/>
    <circle cx="432" cy="412" r="16" fill="#16A34A"/><text x="432" y="417" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#FFF">5</text>
    <text x="515" y="410" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#166534">Connect EC2</text>
    <text x="515" y="428" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">whoami = ec2-user</text>
  </g>
  <line x1="400" y1="460" x2="400" y2="498" stroke="#475569" stroke-width="2" marker-end="url(#a)"/>

  <!-- Phase 3 -->
  <rect x="40" y="498" width="720" height="148" rx="12" fill="#FFFBEB" stroke="#D97706" stroke-width="2"/>
  <text x="56" y="524" font-family="{FONT}" font-size="14" font-weight="700" fill="#92400E">Phase 3 — Linux Skills</text>
  <text x="56" y="542" font-family="{FONT}" font-size="11" fill="#64748B">Steps 6–7 · Remote terminal on EC2 · ~15 min</text>
  <g>
    <rect x="180" y="556" width="200" height="72" rx="10" fill="#FFFFFF" stroke="#D97706"/>
    <circle cx="202" cy="580" r="16" fill="#D97706"/><text x="202" y="585" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#FFF">6</text>
    <text x="285" y="578" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#92400E">Scripts</text>
    <text x="285" y="596" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">chmod · ./</text>
  </g>
  <line x1="380" y1="580" x2="410" y2="580" stroke="#D97706" stroke-width="2" marker-end="url(#a)"/>
  <g>
    <rect x="410" y="556" width="200" height="72" rx="10" fill="#FFFFFF" stroke="#D97706"/>
    <circle cx="432" cy="580" r="16" fill="#D97706"/><text x="432" y="585" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#FFF">7</text>
    <text x="515" y="578" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#92400E">SetUID Find</text>
    <text x="515" y="596" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">privilege risk</text>
  </g>
  <line x1="400" y1="628" x2="400" y2="666" stroke="#475569" stroke-width="2" marker-end="url(#a)"/>

  <!-- Phase 4 -->
  <rect x="40" y="666" width="720" height="120" rx="12" fill="#FEE2E2" stroke="#DC2626" stroke-width="2"/>
  <text x="56" y="692" font-family="{FONT}" font-size="14" font-weight="700" fill="#991B1B">Phase 4 — Web Service</text>
  <text x="56" y="710" font-family="{FONT}" font-size="11" fill="#64748B">Step 8 · nginx + browser test · ~15 min</text>
  <g>
    <rect x="300" y="724" width="200" height="72" rx="10" fill="#FFFFFF" stroke="#DC2626"/>
    <circle cx="322" cy="748" r="16" fill="#DC2626"/><text x="322" y="753" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#FFF">8</text>
    <text x="405" y="746" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#991B1B">nginx + logs</text>
    <text x="405" y="764" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">access.log telemetry</text>
  </g>
  <line x1="400" y1="796" x2="400" y2="812" stroke="#16A34A" stroke-width="2" marker-end="url(#a)"/>

  <rect x="320" y="812" width="160" height="48" rx="24" fill="#16A34A"/>
  <text x="400" y="840" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#FFFFFF">LAB DONE</text>

  <rect x="40" y="868" width="720" height="28" rx="8" fill="#0F172A"/>
  <text x="400" y="887" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#F8FAFC">Result: EC2 in AWS + SSH access + Linux skills + nginx logs for Lab 1.2</text>
</svg>
""")


write("01-architecture.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 860 520" role="img" aria-label="Lab 1.1 architecture">
  <defs>
    <marker id="ab" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8Z" fill="#2563EB"/></marker>
    <marker id="ag" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8Z" fill="#16A34A"/></marker>
    <linearGradient id="aws" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#FF9900"/><stop offset="100%" stop-color="#E65100"/></linearGradient>
  </defs>
  <rect width="860" height="520" fill="#F8FAFC"/>
  <rect x="20" y="20" width="820" height="480" rx="14" fill="#FFF" stroke="#CBD5E1" stroke-width="2"/>

  <rect x="36" y="36" width="788" height="48" rx="10" fill="#0F172A"/>
  <text x="430" y="66" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="#FFF">Cloud Lab Architecture</text>

  <rect x="36" y="96" width="788" height="36" rx="8" fill="#E0F2FE" stroke="#0284C7"/>
  <text x="430" y="119" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="600" fill="#0369A1">Internet</text>

  <rect x="36" y="148" width="200" height="200" rx="12" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
  <text x="136" y="178" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#1E3A8A">Your Windows PC</text>
  <text x="136" y="200" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#475569">VS Code Remote SSH</text>
  <text x="136" y="218" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#475569">soc-lab-key.pem</text>
  <text x="136" y="236" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#475569">Web browser</text>
  <rect x="52" y="256" width="76" height="28" rx="6" fill="#2563EB"/>
  <text x="90" y="275" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#FFF">SSH 22</text>
  <rect x="144" y="256" width="76" height="28" rx="6" fill="#16A34A"/>
  <text x="174" y="275" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#FFF">HTTP 80</text>

  <rect x="260" y="136" width="564" height="316" rx="12" fill="#FAFAFA" stroke="#64748B" stroke-width="2" stroke-dasharray="6 4"/>
  <text x="280" y="168" font-family="{FONT}" font-size="12" font-weight="700" fill="#475569">VPC — Virtual Private Cloud</text>

  <rect x="280" y="184" width="524" height="260" rx="10" fill="#FFF7ED" stroke="#F59E0B" stroke-width="2"/>
  <text x="300" y="210" font-family="{FONT}" font-size="13" font-weight="700" fill="#92400E">Security Group (firewall)</text>
  <rect x="300" y="222" width="100" height="26" rx="6" fill="#DC2626"/>
  <text x="350" y="240" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#FFF">ALLOW 22</text>
  <rect x="410" y="222" width="100" height="26" rx="6" fill="#DC2626"/>
  <text x="460" y="240" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#FFF">ALLOW 80</text>
  <rect x="520" y="222" width="90" height="26" rx="6" fill="#64748B"/>
  <text x="565" y="240" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#FFF">DENY rest</text>

  <rect x="300" y="268" width="484" height="160" rx="12" fill="url(#aws)" stroke="#C2410C" stroke-width="2"/>
  <text x="542" y="300" text-anchor="middle" font-family="{FONT}" font-size="16" font-weight="700" fill="#FFF">EC2 — Elastic Compute Cloud</text>
  <text x="542" y="322" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#FFF7ED">Amazon Linux 2023 · t2.medium</text>
  <rect x="320" y="340" width="140" height="68" rx="8" fill="rgba(255,255,255,0.25)" stroke="#FFF"/>
  <text x="390" y="368" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#FFF">nginx :80</text>
  <text x="390" y="386" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#FFF7ED">web service</text>
  <rect x="480" y="340" width="284" height="68" rx="8" fill="rgba(255,255,255,0.25)" stroke="#FFF"/>
  <text x="622" y="376" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#FFF">/var/log/nginx/access.log</text>

  <path d="M236 220 C270 220 280 280" fill="none" stroke="#2563EB" stroke-width="3" marker-end="url(#ab)"/>
  <text x="248" y="248" font-family="{FONT}" font-size="10" font-weight="600" fill="#2563EB">SSH :22</text>
  <path d="M236 290 C270 290 280 340" fill="none" stroke="#16A34A" stroke-width="3" marker-end="url(#ag)"/>
  <text x="248" y="318" font-family="{FONT}" font-size="10" font-weight="600" fill="#16A34A">HTTP :80</text>
  <rect x="620" y="268" width="120" height="36" rx="8" fill="#FFF" stroke="#64748B"/>
  <text x="680" y="284" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#334155">Public IP</text>
  <text x="680" y="298" text-anchor="middle" font-family="{FONT}" font-size="9" fill="#64748B">from Step 3</text>

  <rect x="36" y="468" width="788" height="24" rx="6" fill="#F1F5F9"/>
  <text x="430" y="484" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">Blue = SSH (Secure Shell) · Green = HTTP (Hypertext Transfer Protocol) · Orange = AWS resources</text>
</svg>
""")


write("02-vpc-networking.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 400" role="img" aria-label="VPC networking">
  <defs>
    <marker id="va" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8Z" fill="#334155"/></marker>
  </defs>
  <rect width="820" height="400" fill="#F8FAFC"/>
  <text x="410" y="36" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="#0F172A">VPC — Virtual Private Cloud</text>
  <text x="410" y="58" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#64748B">Your isolated network boundary inside AWS</text>

  <rect x="40" y="80" width="740" height="240" rx="14" fill="#FFF" stroke="#64748B" stroke-width="2"/>
  <text x="410" y="108" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="600" fill="#475569">Subnet (network slice inside VPC)</text>

  <rect x="80" y="128" width="300" height="168" rx="10" fill="#FEE2E2" stroke="#DC2626" stroke-width="2"/>
  <text x="230" y="158" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#991B1B">Security Group</text>
  <text x="230" y="182" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#7F1D1D">Virtual firewall rules</text>
  <rect x="110" y="198" width="110" height="28" rx="6" fill="#DC2626"/>
  <text x="165" y="217" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#FFF">ALLOW TCP 22</text>
  <rect x="230" y="198" width="110" height="28" rx="6" fill="#DC2626"/>
  <text x="285" y="217" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#FFF">ALLOW TCP 80</text>
  <rect x="110" y="238" width="230" height="28" rx="6" fill="#64748B"/>
  <text x="225" y="257" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#FFF">DENY all other traffic</text>

  <rect x="440" y="148" width="300" height="128" rx="12" fill="#DCFCE7" stroke="#16A34A" stroke-width="2"/>
  <text x="590" y="188" text-anchor="middle" font-family="{FONT}" font-size="15" font-weight="700" fill="#166534">EC2 Instance</text>
  <text x="590" y="212" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#15803D">Traffic must match SG rules</text>
  <text x="590" y="232" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#15803D">Attached at launch</text>
  <line x1="380" y1="212" x2="435" y2="212" stroke="#334155" stroke-width="3" marker-end="url(#va)"/>
  <text x="408" y="200" text-anchor="middle" font-family="{FONT}" font-size="10" font-weight="600" fill="#334155">Ingress</text>

  <rect x="40" y="336" width="740" height="48" rx="10" fill="#EFF6FF" stroke="#BFDBFE"/>
  <text x="410" y="358" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#1E40AF">Think of the Security Group as a bouncer — only listed ports enter.</text>
  <text x="410" y="376" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">SG = Security Group · TCP = Transmission Control Protocol · Ingress = incoming traffic</text>
</svg>
""")


write("03-ssh-keys.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 320" role="img" aria-label="SSH key authentication">
  <defs>
    <marker id="sa" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8Z" fill="#2563EB"/></marker>
  </defs>
  <rect width="820" height="320" fill="#F8FAFC"/>
  <text x="410" y="36" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="#0F172A">SSH — Secure Shell</text>
  <text x="410" y="58" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#64748B">Key-based authentication (no password)</text>

  <rect x="40" y="84" width="240" height="180" rx="12" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
  <text x="160" y="112" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#1E40AF">Your PC</text>
  <rect x="68" y="128" width="184" height="56" rx="8" fill="#FFF" stroke="#93C5FD" stroke-width="2"/>
  <text x="88" y="152" font-family="{FONT}" font-size="16" fill="#2563EB">🔑</text>
  <text x="160" y="152" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#334155">soc-lab-key.pem</text>
  <text x="160" y="172" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">PEM = private key (secret)</text>
  <text x="160" y="228" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">Never share this file</text>

  <rect x="540" y="84" width="240" height="180" rx="12" fill="#DCFCE7" stroke="#16A34A" stroke-width="2"/>
  <text x="660" y="112" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#166534">EC2 Server</text>
  <rect x="568" y="128" width="184" height="56" rx="8" fill="#FFF" stroke="#86EFAC" stroke-width="2"/>
  <text x="588" y="152" font-family="{FONT}" font-size="16" fill="#16A34A">🔒</text>
  <text x="660" y="156" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#334155">authorized_keys</text>
  <text x="660" y="172" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Public key (from AWS)</text>
  <text x="660" y="228" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">Login: ec2-user</text>

  <rect x="310" y="130" width="120" height="88" rx="10" fill="#FFF" stroke="#2563EB" stroke-dasharray="5 3"/>
  <text x="410" y="162" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="600" fill="#2563EB">Encrypted</text>
  <text x="410" y="182" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="600" fill="#2563EB">tunnel</text>
  <text x="410" y="204" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">Port 22</text>
  <line x1="280" y1="174" x2="290" y2="174" stroke="#2563EB" stroke-width="2" marker-end="url(#sa)"/>
  <line x1="530" y1="174" x2="540" y2="174" stroke="#2563EB" stroke-width="2" marker-end="url(#sa)"/>

  <rect x="40" y="280" width="740" height="28" rx="8" fill="#EFF6FF"/>
  <text x="410" y="299" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#1E40AF">VS Code Remote-SSH uses the private key to open terminal, files, and editor on EC2</text>
</svg>
""")


write("04-chmod-flow.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 260" role="img" aria-label="chmod permission flow">
  <defs>
    <marker id="ca" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8Z" fill="#475569"/></marker>
  </defs>
  <rect width="820" height="260" fill="#F8FAFC"/>
  <text x="410" y="32" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="#0F172A">Linux Permissions — chmod +x</text>
  <text x="410" y="52" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">Make a script executable, then run it</text>

  <circle cx="90" cy="110" r="20" fill="#F59E0B"/><text x="90" y="116" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#FFF">1</text>
  <rect x="40" y="140" width="100" height="70" rx="10" fill="#FEF3C7" stroke="#F59E0B" stroke-width="2"/>
  <text x="90" y="168" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#92400E">hello.sh</text>
  <text x="90" y="188" text-anchor="middle" font-family="monospace" font-size="11" fill="#78350F">-rw-r--r--</text>

  <line x1="140" y1="175" x2="175" y2="175" stroke="#475569" stroke-width="2" marker-end="url(#ca)"/>
  <circle cx="210" cy="175" r="20" fill="#2563EB"/><text x="210" y="181" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#FFF">2</text>
  <text x="210" y="210" text-anchor="middle" font-family="monospace" font-size="12" fill="#1E40AF">chmod +x</text>

  <line x1="230" y1="175" x2="265" y2="175" stroke="#475569" stroke-width="2" marker-end="url(#ca)"/>
  <circle cx="300" cy="175" r="20" fill="#16A34A"/><text x="300" y="181" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#FFF">3</text>
  <rect x="250" y="140" width="100" height="70" rx="10" fill="#DCFCE7" stroke="#22C55E" stroke-width="2"/>
  <text x="300" y="168" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#166534">hello.sh</text>
  <text x="300" y="188" text-anchor="middle" font-family="monospace" font-size="11" fill="#15803D">-rwxr-xr-x</text>

  <line x1="350" y1="175" x2="385" y2="175" stroke="#475569" stroke-width="2" marker-end="url(#ca)"/>
  <circle cx="420" cy="175" r="20" fill="#7C3AED"/><text x="420" y="181" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="700" fill="#FFF">4</text>
  <rect x="370" y="140" width="100" height="70" rx="10" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
  <text x="420" y="168" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#1E40AF">./hello.sh</text>
  <text x="420" y="188" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#334155">Hello SOC</text>

  <rect x="520" y="130" width="260" height="90" rx="10" fill="#FFF" stroke="#E2E8F0"/>
  <text x="650" y="152" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#334155">Permission bits (rwx)</text>
  <text x="560" y="172" font-family="monospace" font-size="11" fill="#64748B">owner</text>
  <text x="620" y="172" font-family="monospace" font-size="11" fill="#64748B">group</text>
  <text x="680" y="172" font-family="monospace" font-size="11" fill="#64748B">other</text>
  <rect x="548" y="180" width="52" height="22" rx="4" fill="#FEF3C7" stroke="#F59E0B"/>
  <text x="574" y="195" text-anchor="middle" font-family="monospace" font-size="10" fill="#92400E">rw-</text>
  <rect x="608" y="180" width="52" height="22" rx="4" fill="#FEF3C7" stroke="#F59E0B"/>
  <text x="634" y="195" text-anchor="middle" font-family="monospace" font-size="10" fill="#92400E">r--</text>
  <rect x="668" y="180" width="52" height="22" rx="4" fill="#DCFCE7" stroke="#22C55E"/>
  <text x="694" y="195" text-anchor="middle" font-family="monospace" font-size="10" fill="#166534">r-x</text>
  <text x="650" y="218" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">chmod +x adds execute (x) for all</text>

  <rect x="40" y="236" width="740" height="20" rx="4" fill="#EFF6FF"/>
  <text x="410" y="250" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">chmod = change mode · only executable files can run with ./hello.sh</text>
</svg>
""")


write("05-setuid-flow.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 300" role="img" aria-label="SetUID privilege flow">
  <defs>
    <marker id="ua" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8Z" fill="#475569"/></marker>
  </defs>
  <rect width="820" height="300" fill="#F8FAFC"/>
  <text x="410" y="36" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="#0F172A">SetUID — Set User ID</text>
  <text x="410" y="58" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#64748B">Program runs as the file owner (often root), not who launched it</text>

  <rect x="60" y="88" width="180" height="100" rx="12" fill="#DBEAFE" stroke="#2563EB" stroke-width="2"/>
  <text x="150" y="120" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="600" fill="#1E40AF">ec2-user</text>
  <text x="150" y="142" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">normal privilege</text>
  <text x="150" y="162" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">runs passwd</text>

  <rect x="320" y="98" width="180" height="100" rx="12" fill="#FEE2E2" stroke="#EF4444" stroke-width="2"/>
  <text x="410" y="128" text-anchor="middle" font-family="{FONT}" font-size="13" font-weight="600" fill="#991B1B">/usr/bin/passwd</text>
  <text x="410" y="152" text-anchor="middle" font-family="monospace" font-size="12" fill="#7F1D1D">-rwsr-xr-x</text>
  <text x="410" y="172" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#7F1D1D">s = SetUID bit</text>

  <rect x="580" y="88" width="180" height="100" rx="12" fill="#DCFCE7" stroke="#16A34A" stroke-width="2"/>
  <text x="670" y="120" text-anchor="middle" font-family="{FONT}" font-size="14" font-weight="600" fill="#166534">root</text>
  <text x="670" y="142" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">effective user</text>
  <text x="670" y="162" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#64748B">elevated run</text>

  <path d="M240 138 L310 138" fill="none" stroke="#475569" stroke-width="2.5" marker-end="url(#ua)"/>
  <path d="M500 138 L555 138" fill="none" stroke="#475569" stroke-width="2.5" marker-end="url(#ua)"/>

  <rect x="60" y="210" width="700" height="68" rx="10" fill="#FEF3C7" stroke="#F59E0B" stroke-width="2"/>
  <text x="410" y="236" text-anchor="middle" font-family="{FONT}" font-size="12" font-weight="600" fill="#92400E">Defender action: inventory SetUID binaries on every Linux host</text>
  <text x="410" y="258" text-anchor="middle" font-family="monospace" font-size="10" fill="#78350F">find / -perm -4000 -exec ls -l &#123;&#125; &#92;; 2&gt;/dev/null</text>
</svg>
""")


write("06-nginx-telemetry.svg", f"""
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 880 300" role="img" aria-label="nginx telemetry flow">
  <defs>
    <marker id="na" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8Z" fill="#475569"/></marker>
  </defs>
  <rect width="880" height="300" fill="#F8FAFC"/>
  <text x="440" y="36" text-anchor="middle" font-family="{FONT}" font-size="18" font-weight="700" fill="#0F172A">HTTP Request to Telemetry</text>
  <text x="440" y="58" text-anchor="middle" font-family="{FONT}" font-size="12" fill="#64748B">Each web request creates a log line for future AI detection labs</text>

  <circle cx="100" cy="130" r="24" fill="#2563EB"/>
  <text x="100" y="136" text-anchor="middle" font-family="{FONT}" font-size="16" font-weight="700" fill="#FFF">1</text>
  <rect x="50" y="168" width="100" height="56" rx="8" fill="#DBEAFE" stroke="#2563EB"/>
  <text x="100" y="192" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#1E40AF">Browser</text>
  <text x="100" y="210" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">HTTP GET /</text>

  <line x1="124" y1="130" x2="176" y2="130" stroke="#475569" stroke-width="2" marker-end="url(#na)"/>

  <circle cx="240" cy="130" r="24" fill="#D97706"/>
  <text x="240" y="136" text-anchor="middle" font-family="{FONT}" font-size="16" font-weight="700" fill="#FFF">2</text>
  <rect x="190" y="168" width="100" height="56" rx="8" fill="#FFF7ED" stroke="#F59E0B"/>
  <text x="240" y="192" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#92400E">nginx</text>
  <text x="240" y="210" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#78350F">port 80</text>

  <line x1="264" y1="130" x2="316" y2="130" stroke="#475569" stroke-width="2" marker-end="url(#na)"/>

  <circle cx="380" cy="130" r="24" fill="#64748B"/>
  <text x="380" y="136" text-anchor="middle" font-family="{FONT}" font-size="16" font-weight="700" fill="#FFF">3</text>
  <rect x="320" y="168" width="120" height="56" rx="8" fill="#F1F5F9" stroke="#64748B"/>
  <text x="380" y="192" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#334155">access.log</text>
  <text x="380" y="210" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">1 line / hit</text>

  <line x1="404" y1="130" x2="456" y2="130" stroke="#475569" stroke-width="2" marker-end="url(#na)"/>

  <circle cx="520" cy="130" r="24" fill="#16A34A"/>
  <text x="520" y="136" text-anchor="middle" font-family="{FONT}" font-size="16" font-weight="700" fill="#FFF">4</text>
  <rect x="460" y="168" width="120" height="56" rx="8" fill="#DCFCE7" stroke="#22C55E"/>
  <text x="520" y="192" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#166534">Lab 1.2+</text>
  <text x="520" y="210" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#15803D">AI detection</text>

  <rect x="620" y="108" width="220" height="116" rx="10" fill="#FFF" stroke="#CBD5E1"/>
  <text x="730" y="132" text-anchor="middle" font-family="{FONT}" font-size="11" font-weight="600" fill="#334155">Sample log line</text>
  <text x="730" y="158" text-anchor="middle" font-family="monospace" font-size="9" fill="#64748B">192.0.2.1 - - [date] "GET /"</text>
  <text x="730" y="176" text-anchor="middle" font-family="monospace" font-size="9" fill="#64748B">200 612 "-" "Mozilla/..."</text>
  <text x="730" y="204" text-anchor="middle" font-family="{FONT}" font-size="10" fill="#64748B">IP · time · request · status</text>

  <rect x="40" y="252" width="800" height="36" rx="8" fill="#EFF6FF" stroke="#BFDBFE"/>
  <text x="440" y="274" text-anchor="middle" font-family="{FONT}" font-size="11" fill="#1E40AF">Telemetry = observable data from your system · nginx access.log is your first detection data source</text>
</svg>
""")

print("Wrote 7 improved diagrams")
