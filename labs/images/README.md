# Lab images

Visual assets for the SOC lab guides. Lab markdown uses **relative** paths: `images/<filename>` (from each file in `labs/`).

## Architecture diagrams

Each diagram has a source `.svg` and a rendered `.png`. Lab guides reference the **PNG** for reliable rendering on GitHub and in VS Code preview.

| PNG (used in labs) | SVG (source) | Lab |
|--------------------|--------------|-----|
| `lab-1.1-architecture.png` | `lab-1.1-architecture.svg` | 1.1 |
| `lab-1.2-attack-triage-flow.png` | `lab-1.2-attack-triage-flow.svg` | 1.2 |
| `lab-1.3-detection-flow.png` | `lab-1.3-detection-flow.svg` | 1.3 |
| `lab-1.3-s3-defender-loop.png` | `lab-1.3-s3-defender-loop.svg` | 1.3 |
| `lab-2.1-cloudwatch-pipeline.png` | `lab-2.1-cloudwatch-pipeline.svg` | 2.1 |
| `lab-2.2-detection-pipeline.png` | `lab-2.2-detection-pipeline.svg` | 2.2 |
| `lab-2.3-capstone-loop.png` | `lab-2.3-capstone-loop.svg` | 2.3 |
| `lab-roadmap-overview.png` | `lab-roadmap-overview.svg` | labs/README.md |
| `lab-defender-maturity.png` | `lab-defender-maturity.svg` | labs/README.md |
| `lab-ai-layers.png` | `lab-ai-layers.svg` | labs/README.md |

To regenerate PNGs after editing an SVG (from this directory):

```bash
npm install @resvg/resvg-js --no-save
node -e "const{Resvg}=require('@resvg/resvg-js');const fs=require('fs');for(const f of fs.readdirSync('.').filter(x=>x.endsWith('.svg')&&x.startsWith('lab-'))){const png=f.replace('.svg','.png');fs.writeFileSync(png,new Resvg(fs.readFileSync(f,'utf8'),{fitTo:{mode:'width',value:920}}).render().asPng());console.log('wrote',png);}"
```

## Console screenshots (PNG)

| File | Used in |
|------|---------|
| `aws-cloudshell-download.png` | Lab 1.1 |
| `remote-ssh.png` | Lab 1.1 |
| `remote-ssh-connect.png` | Lab 1.1 |
| `remote-ssh-open-home.png` | Lab 1.1 |
| `ssh-new-terminal.png` | Lab 1.1 |
| `bedrock-api-keys.png` | Lab 1.2 |
| `guardduty-enable.png` | Lab 1.3 |
| `security-hub-get-started.png` | Lab 1.3 |
| `guard-duty-findings.png` | Lab 1.3 |
| `security-hub-all-findings.png` | Lab 1.3 |
| `log-analytics-build-query.png` | Lab 2.1 |
| `log-analytics-file-view.png` | Lab 2.1 |
| `investigation-query.png` | Labs 2.1, 2.3 |
| `create-investigation.png` | Labs 2.1, 2.3 |
| `create-log-filter.png` | Labs 2.2, 2.3 |
| `log-filter-metric.png` | Lab 2.2 |
| `metric-details.png` | Lab 2.2 |
| `new-widget.png` | Lab 2.2 |
| `graphed-metrics.png` | Lab 2.2 |
| `log-widget.png` | Lab 2.2 |
| `Generate-new-query.png` | Lab 2.2 |
| `create-alarm.png` | Labs 2.2, 2.3 |

> Do not add API keys, `.pem` files, instance IPs, or account IDs to images committed to this repo.
