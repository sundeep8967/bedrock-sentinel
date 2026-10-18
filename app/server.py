import os
import sys
import json
from flask import Flask, render_template_string, jsonify, request

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from telemetry import CloudTelemetryCollector
from agent import BedrockSentinelAgent
from iac_engine import IaCEngine

app = Flask(__name__)
root_dir = os.path.dirname(current_dir)
tf_file = os.path.join(root_dir, "terraform_demo", "main.tf")

collector = CloudTelemetryCollector(region="us-east-1")
agent = BedrockSentinelAgent()
iac = IaCEngine(tf_file)

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>BedrockSentinel — Autonomous AWS Cloud Cost & IaC Agent</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-dark: #070913;
      --card-bg: rgba(18, 24, 38, 0.75);
      --card-border: rgba(255, 255, 255, 0.08);
      --card-hover: rgba(30, 41, 59, 0.85);
      --accent-cyan: #00F2FE;
      --accent-blue: #4FACFE;
      --accent-purple: #8B5CF6;
      --accent-emerald: #10B981;
      --accent-rose: #F43F5E;
      --accent-amber: #F59E0B;
      --text-main: #F8FAFC;
      --text-muted: #94A3B8;
      --font-sans: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
      --font-mono: 'JetBrains Mono', monospace;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      background: radial-gradient(circle at 50% 0%, #151C33 0%, var(--bg-dark) 70%);
      color: var(--text-main);
      font-family: var(--font-sans);
      min-height: 100vh;
      line-height: 1.5;
      padding-bottom: 60px;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 24px;
    }

    header {
      padding: 32px 0 24px;
      border-bottom: 1px solid var(--card-border);
      position: sticky;
      top: 0;
      backdrop-filter: blur(16px);
      z-index: 100;
      background: rgba(7, 9, 19, 0.85);
    }

    .header-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .logo-group {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .logo-badge {
      width: 44px;
      height: 44px;
      border-radius: 12px;
      background: linear-gradient(135deg, var(--accent-cyan), var(--accent-purple));
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
      box-shadow: 0 0 20px rgba(0, 242, 254, 0.35);
    }

    .logo-text h1 {
      font-size: 1.45rem;
      font-weight: 700;
      letter-spacing: -0.02em;
      background: linear-gradient(to right, #FFFFFF, #94A3B8);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .logo-text p {
      font-size: 0.82rem;
      color: var(--accent-cyan);
      font-weight: 500;
      letter-spacing: 0.05em;
      text-transform: uppercase;
    }

    .badge-hackathon {
      background: rgba(139, 92, 246, 0.15);
      border: 1px solid rgba(139, 92, 246, 0.4);
      color: #C4B5FD;
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .badge-hackathon span {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--accent-emerald);
      box-shadow: 0 0 8px var(--accent-emerald);
      animation: pulse 2s infinite;
    }

    @keyframes pulse {
      0% { opacity: 0.4; }
      50% { opacity: 1; }
      100% { opacity: 0.4; }
    }

    .hero-banner {
      margin: 36px 0 28px;
      background: linear-gradient(135deg, rgba(21, 28, 51, 0.6), rgba(18, 24, 38, 0.4));
      border: 1px solid var(--card-border);
      border-radius: 20px;
      padding: 36px;
      position: relative;
      overflow: hidden;
      backdrop-filter: blur(12px);
    }

    .hero-banner::before {
      content: '';
      position: absolute;
      top: -100px;
      right: -100px;
      width: 300px;
      height: 300px;
      background: radial-gradient(circle, rgba(0, 242, 254, 0.15) 0%, transparent 70%);
      pointer-events: none;
    }

    .hero-banner h2 {
      font-size: 2.1rem;
      font-weight: 800;
      line-height: 1.2;
      margin-bottom: 12px;
      letter-spacing: -0.02em;
    }

    .hero-banner p {
      font-size: 1.05rem;
      color: var(--text-muted);
      max-width: 780px;
      margin-bottom: 24px;
    }

    .btn-action {
      background: linear-gradient(135deg, var(--accent-cyan), var(--accent-blue));
      color: #070913;
      border: none;
      padding: 14px 28px;
      border-radius: 12px;
      font-weight: 700;
      font-size: 1rem;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 10px;
      transition: all 0.25s ease;
      box-shadow: 0 4px 20px rgba(0, 242, 254, 0.3);
    }

    .btn-action:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 30px rgba(0, 242, 254, 0.45);
    }

    .btn-action:active {
      transform: translateY(0);
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 20px;
      margin-bottom: 36px;
    }

    .stat-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 24px;
      backdrop-filter: blur(10px);
      transition: border-color 0.2s ease;
    }

    .stat-card:hover {
      border-color: rgba(255, 255, 255, 0.2);
    }

    .stat-label {
      font-size: 0.85rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-bottom: 8px;
    }

    .stat-val {
      font-size: 2rem;
      font-weight: 800;
      font-family: var(--font-mono);
      letter-spacing: -0.02em;
    }

    .stat-sub {
      font-size: 0.85rem;
      margin-top: 6px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .val-cyan { color: var(--accent-cyan); }
    .val-emerald { color: var(--accent-emerald); }
    .val-rose { color: var(--accent-rose); }
    .val-purple { color: #C4B5FD; }

    .section-title {
      font-size: 1.35rem;
      font-weight: 700;
      margin: 36px 0 18px;
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .resources-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 20px;
    }

    .resource-card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 16px;
      padding: 22px;
      backdrop-filter: blur(10px);
      position: relative;
    }

    .res-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 14px;
    }

    .res-title {
      font-weight: 700;
      font-size: 1.05rem;
    }

    .res-type {
      font-family: var(--font-mono);
      font-size: 0.75rem;
      color: var(--accent-cyan);
      background: rgba(0, 242, 254, 0.1);
      padding: 3px 8px;
      border-radius: 6px;
    }

    .res-status {
      font-size: 0.75rem;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 9999px;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    .status-bad {
      background: rgba(244, 63, 94, 0.15);
      color: var(--accent-rose);
      border: 1px solid rgba(244, 63, 94, 0.3);
    }

    .status-good {
      background: rgba(16, 185, 129, 0.15);
      color: var(--accent-emerald);
      border: 1px solid rgba(16, 185, 129, 0.3);
    }

    .metric-list {
      margin: 14px 0;
      font-size: 0.88rem;
      color: var(--text-muted);
      border-top: 1px solid rgba(255, 255, 255, 0.05);
      padding-top: 12px;
    }

    .metric-item {
      display: flex;
      justify-content: space-between;
      margin-bottom: 6px;
    }

    .metric-item span:last-child {
      font-family: var(--font-mono);
      color: var(--text-main);
      font-weight: 600;
    }

    .remediation-box {
      margin-top: 14px;
      padding: 12px;
      border-radius: 10px;
      background: rgba(139, 92, 246, 0.08);
      border: 1px dashed rgba(139, 92, 246, 0.3);
      font-size: 0.85rem;
    }

    .remediation-box strong {
      color: #C4B5FD;
      display: block;
      margin-bottom: 4px;
    }

    .diff-container {
      background: #0D1117;
      border: 1px solid var(--card-border);
      border-radius: 16px;
      overflow: hidden;
      margin-top: 24px;
      font-family: var(--font-mono);
      font-size: 0.88rem;
    }

    .diff-header {
      background: #161B22;
      padding: 12px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }

    .diff-filename {
      color: #58A6FF;
      font-weight: 600;
    }

    .diff-body {
      padding: 18px 20px;
      max-height: 480px;
      overflow-y: auto;
      white-space: pre;
      line-height: 1.6;
    }

    .line-add { color: #3FB950; background: rgba(46, 160, 67, 0.15); display: block; padding: 1px 8px; border-radius: 4px; }
    .line-del { color: #F85149; background: rgba(248, 81, 73, 0.15); display: block; padding: 1px 8px; border-radius: 4px; }
    .line-info { color: #8B949E; }

    footer {
      text-align: center;
      margin-top: 50px;
      color: var(--text-muted);
      font-size: 0.85rem;
    }
  </style>
</head>
<body>

  <header>
    <div class="container header-content">
      <div class="logo-group">
        <div class="logo-badge">☁️</div>
        <div class="logo-text">
          <h1>BedrockSentinel</h1>
          <p>Autonomous FinOps & IaC Agent</p>
        </div>
      </div>
      <div class="badge-hackathon">
        <span></span> Build, Ship, Shape: Amazon Developer Hackathon
      </div>
    </div>
  </header>

  <div class="container">
    <div class="hero-banner">
      <h2>Transform Cloud Waste into 1-Click Pull Requests</h2>
      <p>
        BedrockSentinel monitors AWS CloudWatch & Cost Explorer telemetry, reasons over infrastructure using 
        <strong>Amazon Bedrock (Claude 3.5 Sonnet / Amazon Nova)</strong>, and safely auto-patches HashiCorp Terraform repositories.
      </p>
      <button class="btn-action" id="run-optimization-btn" onclick="runOptimization()">
        ⚡ Run Bedrock FinOps Reasoning Agent
      </button>
    </div>

    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-label">Current Monthly Burn</div>
        <div class="stat-val val-rose" id="current-burn">$800.00</div>
        <div class="stat-sub" style="color: var(--accent-rose);">Across 3 monitored AWS workloads</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Projected Optimized Burn</div>
        <div class="stat-val val-emerald" id="optimized-burn">$160.00</div>
        <div class="stat-sub val-emerald">Post auto-remediation</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Net Monthly Savings</div>
        <div class="stat-val val-cyan" id="monthly-savings">$640.00 / mo</div>
        <div class="stat-sub val-cyan">80.0% spend reduction</div>
      </div>
      <div class="stat-card">
        <div class="stat-label">Annualized Run-Rate Savings</div>
        <div class="stat-val val-purple" id="annual-savings">$7,680.00</div>
        <div class="stat-sub" style="color: #C4B5FD;">Sustained annualized FinOps ROI</div>
      </div>
    </div>

    <div class="section-title">
      📡 Live Telemetry & Architectural Diagnosis
    </div>

    <div class="resources-grid" id="resources-container">
      <!-- Populated via Javascript -->
    </div>

    <div class="section-title">
      📝 Automated Git Pull Request & Unified Terraform Diff
    </div>

    <div class="diff-container">
      <div class="diff-header">
        <div class="diff-filename">terraform_demo/main.tf</div>
        <div style="font-size: 0.8rem; color: var(--text-muted);">Verified Non-Destructive Diff</div>
      </div>
      <div class="diff-body" id="diff-output">Click 'Run Bedrock FinOps Reasoning Agent' above to compute live remediation diff.</div>
    </div>

    <footer>
      BedrockSentinel • Built for the Amazon Developer Hackathon • Powered by Amazon Bedrock & HashiCorp Terraform
    </footer>
  </div>

  <script>
    async function loadTelemetry() {
      const res = await fetch('/api/telemetry');
      const data = await res.json();
      renderResources(data);
    }

    function renderResources(resources, remediations = null) {
      const container = document.getElementById('resources-container');
      container.innerHTML = '';

      resources.forEach(r => {
        let remHtml = '';
        if (remediations) {
          const rem = remediations.find(item => item.resource_id === r.resource_id);
          if (rem) {
            remHtml = `
              <div class="remediation-box">
                <strong>💡 Bedrock Recommendation:</strong>
                ${rem.action} ➔ <code>${rem.recommended_sku}</code> (Save $${rem.monthly_savings_usd.toFixed(2)}/mo)
                <p style="margin-top: 4px; color: #94A3B8;">${rem.justification}</p>
              </div>
            `;
          }
        }

        let metricsHtml = '';
        for (const [k, v] of Object.entries(r.metrics)) {
          metricsHtml += `<div class="metric-item"><span>${k.replace(/_/g, ' ')}:</span> <span>${v}</span></div>`;
        }

        const card = document.createElement('div');
        card.className = 'resource-card';
        card.innerHTML = `
          <div class="res-header">
            <div>
              <div class="res-title">${r.resource_id}</div>
              <span class="res-type">${r.resource_type} • ${r.current_sku}</span>
            </div>
            <span class="res-status ${r.status.includes('UNDER') || r.status.includes('ORPHAN') || r.status.includes('OVER') ? 'status-bad' : 'status-good'}">
              ${r.status.replace(/_/g, ' ')}
            </span>
          </div>
          <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC; margin-bottom: 8px;">
            $${r.current_cost_usd_monthly.toFixed(2)} <span style="font-size: 0.8rem; color: var(--text-muted); font-weight: 400;">/ month</span>
          </div>
          <div class="metric-list">
            ${metricsHtml}
          </div>
          ${remHtml}
        `;
        container.appendChild(card);
      });
    }

    async function runOptimization() {
      const btn = document.getElementById('run-optimization-btn');
      btn.innerText = '🧠 Bedrock Reasoning in Progress...';
      btn.disabled = true;

      try {
        const res = await fetch('/api/optimize', { method: 'POST' });
        const data = await res.json();

        document.getElementById('current-burn').innerText = `$${data.current_monthly_burn_usd.toFixed(2)}`;
        document.getElementById('optimized-burn').innerText = `$${data.projected_monthly_burn_usd.toFixed(2)}`;
        document.getElementById('monthly-savings').innerText = `$${data.projected_monthly_savings_usd.toFixed(2)} / mo`;
        document.getElementById('annual-savings').innerText = `$${data.annualized_savings_usd.toFixed(2)}`;

        const telRes = await fetch('/api/telemetry');
        const telData = await telRes.json();
        renderResources(telData, data.remediations);

        // Render formatted diff
        const diffBody = document.getElementById('diff-output');
        diffBody.innerHTML = '';
        const lines = data.diff.split('\\n');
        lines.forEach(l => {
          const span = document.createElement('span');
          if (l.startsWith('+') && !l.startsWith('+++')) {
            span.className = 'line-add';
          } else if (l.startsWith('-') && !l.startsWith('---')) {
            span.className = 'line-del';
          } else if (l.startsWith('@@') || l.startsWith('---') || l.startsWith('+++')) {
            span.className = 'line-info';
          }
          span.textContent = l + '\\n';
          diffBody.appendChild(span);
        });

      } catch (err) {
        console.error(err);
      } finally {
        btn.innerText = '⚡ Run Bedrock FinOps Reasoning Agent';
        btn.disabled = false;
      }
    }

    window.onload = loadTelemetry;
  </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/telemetry")
def api_telemetry():
    telemetry = collector.fetch_utilization_metrics()
    return jsonify(telemetry)

@app.route("/api/optimize", methods=["POST"])
def api_optimize():
    telemetry = collector.fetch_utilization_metrics()
    tf_code = iac.read_config()
    result = agent.analyze_and_optimize(telemetry, tf_code)
    diff = iac.generate_unified_diff(tf_code, result["optimized_terraform"])
    pr_text = iac.create_pr_payload(result, diff)
    
    result["diff"] = diff
    result["pr_payload"] = pr_text
    return jsonify(result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    print(f"🚀 BedrockSentinel Web Dashboard serving at http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
