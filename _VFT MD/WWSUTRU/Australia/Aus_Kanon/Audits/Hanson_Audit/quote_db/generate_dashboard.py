#!/usr/bin/env python3
"""
generate_dashboard.py -- build a self-contained HTML dashboard from
quote_verification.db, showing every node's quote next to its Kanon ideal
(never separable -- see README's "always visible" design note), filterable
by status/plane/actor, with KPI cards and a per-plane status breakdown chart.

Run this directly on the local machine (via Desktop Commander or any local
Python) -- it needs real sqlite3 file access, which only works against the
real local disk, not the sandbox's mount of this folder. See README.md.

Usage: python generate_dashboard.py
Output: dashboard.html in this same folder. Open it directly in a browser.
"""
import sqlite3
import json
import os
import html as htmllib

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "quote_verification.db")
OUT_PATH = os.path.join(HERE, "dashboard.html")

STATUS_COLORS = {
    "verified": "#55A868",
    "paraphrased": "#DD8452",
    "fabricated": "#C44E52",
    "needs_hansard": "#8172B3",
    "no_citation": "#937860",
    "unchecked": "#6c757d",
}

def fetch_rows():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.execute(
        """
        SELECT node_id, plane, plane_name, address, vector_name, upsilon, psi,
               hit_fail, quote_in_doc, is_literal_quote, og_node_ideal,
               source_context, citation_key, archive_file, status, fuzzy_score,
               verified_quote, legacy_status, notes
        FROM nodes
        ORDER BY plane, address
        """
    )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def build_html(rows):
    planes = sorted(set(r["plane"] for r in rows))
    statuses = sorted(set(r["status"] for r in rows))
    status_counts = {s: sum(1 for r in rows if r["status"] == s) for s in statuses}

    # per-plane x status grid for the chart
    plane_status = {p: {s: 0 for s in statuses} for p in planes}
    for r in rows:
        plane_status[r["plane"]][r["status"]] += 1

    data_json = json.dumps(rows, ensure_ascii=False)
    plane_labels_json = json.dumps([f"Plane {p}" for p in planes])
    status_json = json.dumps(statuses)
    colors_json = json.dumps(STATUS_COLORS)
    datasets = []
    for s in statuses:
        datasets.append({
            "label": s,
            "data": [plane_status[p][s] for p in planes],
            "backgroundColor": STATUS_COLORS.get(s, "#999999"),
        })
    datasets_json = json.dumps(datasets)

    total = len(rows)
    verified = status_counts.get("verified", 0)
    paraphrased = status_counts.get("paraphrased", 0)
    fabricated = status_counts.get("fabricated", 0)
    other = total - verified - paraphrased - fabricated

    html_out = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Quote Verification Dashboard -- Hanson Audit</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.5.1" crossorigin="anonymous"></script>
<style>
:root {{
  --bg-primary: #f8f9fa; --bg-card: #ffffff; --bg-header: #1a1a2e;
  --text-primary: #212529; --text-secondary: #6c757d; --text-on-dark: #ffffff;
  --positive: #55A868; --warn: #DD8452; --negative: #C44E52; --neutral: #6c757d;
  --gap: 16px; --radius: 8px;
}}
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; background:var(--bg-primary); color:var(--text-primary); line-height:1.5; }}
.dashboard-container {{ max-width:1500px; margin:0 auto; padding:var(--gap); }}
.dashboard-header {{ background:var(--bg-header); color:var(--text-on-dark); padding:20px 24px; border-radius:var(--radius); margin-bottom:var(--gap); display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px; }}
.dashboard-header h1 {{ font-size:20px; font-weight:600; }}
.dashboard-header .sub {{ font-size:12px; color:rgba(255,255,255,0.6); margin-top:2px; }}
.filters {{ display:flex; gap:12px; align-items:center; flex-wrap:wrap; }}
.filter-group {{ display:flex; align-items:center; gap:6px; }}
.filter-group label {{ font-size:12px; color:rgba(255,255,255,0.7); }}
.filter-group select, .filter-group input[type=text] {{ padding:6px 10px; border:1px solid rgba(255,255,255,0.2); border-radius:4px; background:rgba(255,255,255,0.1); color:var(--text-on-dark); font-size:13px; }}
.filter-group select option {{ background:var(--bg-header); color:var(--text-on-dark); }}
.filter-group input::placeholder {{ color:rgba(255,255,255,0.5); }}
.kpi-row {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:var(--gap); margin-bottom:var(--gap); }}
.kpi-card {{ background:var(--bg-card); border-radius:var(--radius); padding:18px 22px; box-shadow:0 1px 3px rgba(0,0,0,0.08); border-left:4px solid var(--neutral); }}
.kpi-card.verified {{ border-left-color:var(--positive); }}
.kpi-card.paraphrased {{ border-left-color:var(--warn); }}
.kpi-card.fabricated {{ border-left-color:var(--negative); }}
.kpi-label {{ font-size:12px; color:var(--text-secondary); text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px; }}
.kpi-value {{ font-size:26px; font-weight:700; }}
.chart-row {{ display:grid; grid-template-columns:1fr; gap:var(--gap); margin-bottom:var(--gap); }}
.chart-container {{ background:var(--bg-card); border-radius:var(--radius); padding:20px 24px; box-shadow:0 1px 3px rgba(0,0,0,0.08); }}
.chart-container h3 {{ font-size:14px; font-weight:600; margin-bottom:16px; }}
.chart-container .chart-wrap {{ position:relative; height:280px; }}
.table-section {{ background:var(--bg-card); border-radius:var(--radius); padding:20px 24px; box-shadow:0 1px 3px rgba(0,0,0,0.08); }}
.table-section h3 {{ font-size:14px; font-weight:600; margin-bottom:12px; }}
.row-count {{ font-size:12px; color:var(--text-secondary); margin-bottom:12px; }}
table.data-table {{ width:100%; border-collapse:collapse; font-size:13px; }}
.data-table thead th {{ text-align:left; padding:8px 10px; border-bottom:2px solid #dee2e6; color:var(--text-secondary); font-weight:600; font-size:11px; text-transform:uppercase; letter-spacing:0.5px; white-space:nowrap; cursor:pointer; user-select:none; }}
.data-table thead th:hover {{ color:var(--text-primary); background:#f8f9fa; }}
.data-table tbody td {{ padding:10px; border-bottom:1px solid #f0f0f0; vertical-align:top; }}
.data-table tbody tr:hover {{ background:#fbfbfb; }}
.badge {{ display:inline-block; padding:2px 8px; border-radius:10px; font-size:11px; font-weight:600; color:#fff; white-space:nowrap; }}
.node-cell {{ min-width:220px; }}
.node-address {{ font-family:ui-monospace,monospace; font-size:11px; color:var(--text-secondary); }}
.node-name {{ font-weight:600; }}
.quote-block {{ min-width:340px; max-width:480px; }}
.quote-block .quote {{ padding:6px 8px; background:#f8f9fa; border-left:3px solid var(--text-secondary); border-radius:3px; margin-bottom:6px; font-size:12.5px; }}
.quote-block .ideal {{ padding:6px 8px; background:#eef4ff; border-left:3px solid #4C72B0; border-radius:3px; font-size:12.5px; }}
.quote-block .tag {{ font-size:10px; text-transform:uppercase; letter-spacing:0.5px; color:var(--text-secondary); margin-bottom:2px; display:block; }}
.score-cell {{ font-family:ui-monospace,monospace; font-size:12px; white-space:nowrap; }}
.hitfail-HIT {{ color:var(--positive); font-weight:700; }}
.hitfail-FAIL {{ color:var(--negative); font-weight:700; }}
footer.dashboard-footer {{ text-align:center; font-size:11px; color:var(--text-secondary); padding:16px 0; }}
@media print {{ .filters {{ display:none; }} }}
</style>
</head>
<body>
<div class="dashboard-container">
  <header class="dashboard-header">
    <div>
      <h1>Quote Verification Dashboard -- Pauline Hanson Audit</h1>
      <div class="sub">Quote and Kanon ideal are always shown together, by design -- never filterable apart</div>
    </div>
    <div class="filters">
      <div class="filter-group">
        <label>Status</label>
        <select id="f-status" onchange="dash.applyFilters()">
          <option value="all">All</option>
        </select>
      </div>
      <div class="filter-group">
        <label>Plane</label>
        <select id="f-plane" onchange="dash.applyFilters()">
          <option value="all">All</option>
        </select>
      </div>
      <div class="filter-group">
        <label>Search</label>
        <input type="text" id="f-search" placeholder="address, name, quote..." oninput="dash.applyFilters()">
      </div>
    </div>
  </header>

  <section class="kpi-row">
    <div class="kpi-card"><div class="kpi-label">Total Nodes</div><div class="kpi-value">{total}</div></div>
    <div class="kpi-card verified"><div class="kpi-label">Verified</div><div class="kpi-value">{verified}</div></div>
    <div class="kpi-card paraphrased"><div class="kpi-label">Paraphrased</div><div class="kpi-value">{paraphrased}</div></div>
    <div class="kpi-card fabricated"><div class="kpi-label">Fabricated</div><div class="kpi-value">{fabricated}</div></div>
    <div class="kpi-card"><div class="kpi-label">Other</div><div class="kpi-value">{other}</div></div>
  </section>

  <section class="chart-row">
    <div class="chart-container">
      <h3>Status by Plane</h3>
      <div class="chart-wrap"><canvas id="plane-chart"></canvas></div>
    </div>
  </section>

  <section class="table-section">
    <h3>Nodes</h3>
    <div class="row-count" id="row-count"></div>
    <div style="overflow-x:auto; max-height:640px; overflow-y:auto;">
      <table class="data-table" id="node-table">
        <thead><tr>
          <th onclick="dash.sort('plane')">Plane</th>
          <th onclick="dash.sort('address')">Address</th>
          <th onclick="dash.sort('vector_name')">Node</th>
          <th onclick="dash.sort('hit_fail')">Hit/Fail</th>
          <th>Quote / Kanon Ideal</th>
          <th onclick="dash.sort('status')">Status</th>
          <th onclick="dash.sort('fuzzy_score')">Score</th>
          <th>Citation</th>
        </tr></thead>
        <tbody id="table-body"></tbody>
      </table>
    </div>
  </section>

  <footer class="dashboard-footer">Generated from quote_verification.db -- regenerate with generate_dashboard.py after any DB change</footer>
</div>

<script>
const DATA = {data_json};
const STATUS_COLORS = {colors_json};
const PLANE_LABELS = {plane_labels_json};
const STATUSES = {status_json};
const CHART_DATASETS = {datasets_json};

function esc(s) {{
  if (s === null || s === undefined) return '';
  return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}}

class Dashboard {{
  constructor(data) {{
    this.rawData = data;
    this.filteredData = data;
    this.sortField = 'plane';
    this.sortDir = 'asc';
    this.init();
  }}
  init() {{
    const statusSel = document.getElementById('f-status');
    [...new Set(this.rawData.map(d => d.status))].sort().forEach(s => {{
      const o = document.createElement('option'); o.value = s; o.textContent = s; statusSel.appendChild(o);
    }});
    const planeSel = document.getElementById('f-plane');
    [...new Set(this.rawData.map(d => d.plane))].sort((a,b)=>a-b).forEach(p => {{
      const o = document.createElement('option'); o.value = p; o.textContent = 'Plane ' + p; planeSel.appendChild(o);
    }});
    this.renderChart();
    this.applyFilters();
  }}
  applyFilters() {{
    const status = document.getElementById('f-status').value;
    const plane = document.getElementById('f-plane').value;
    const search = document.getElementById('f-search').value.toLowerCase();
    this.filteredData = this.rawData.filter(r => {{
      if (status !== 'all' && r.status !== status) return false;
      if (plane !== 'all' && String(r.plane) !== plane) return false;
      if (search) {{
        const hay = (r.address+' '+r.vector_name+' '+(r.quote_in_doc||'')+' '+(r.citation_key||'')).toLowerCase();
        if (!hay.includes(search)) return false;
      }}
      return true;
    }});
    this.renderTable();
  }}
  sort(field) {{
    if (this.sortField === field) {{ this.sortDir = this.sortDir === 'asc' ? 'desc' : 'asc'; }}
    else {{ this.sortField = field; this.sortDir = 'asc'; }}
    this.renderTable();
  }}
  renderChart() {{
    const ctx = document.getElementById('plane-chart').getContext('2d');
    new Chart(ctx, {{
      type: 'bar',
      data: {{ labels: PLANE_LABELS, datasets: CHART_DATASETS.map(ds => ({{...ds, backgroundColor: STATUS_COLORS[ds.label] || '#999'}})) }},
      options: {{
        responsive: true,
        maintainAspectRatio: false,
        plugins: {{ legend: {{ position: 'top', labels: {{ usePointStyle: true, padding: 16 }} }} }},
        scales: {{ x: {{ stacked: true }}, y: {{ stacked: true, beginAtZero: true, ticks: {{ precision: 0 }} }} }}
      }}
    }});
  }}
  renderTable() {{
    const body = document.getElementById('table-body');
    const field = this.sortField, dir = this.sortDir;
    const sorted = [...this.filteredData].sort((a,b) => {{
      let av = a[field], bv = b[field];
      if (av === null || av === undefined) av = '';
      if (bv === null || bv === undefined) bv = '';
      const cmp = av < bv ? -1 : av > bv ? 1 : 0;
      return dir === 'asc' ? cmp : -cmp;
    }});
    document.getElementById('row-count').textContent = `Showing ${{sorted.length}} of ${{this.rawData.length}} nodes`;
    body.innerHTML = sorted.map(r => `
      <tr>
        <td>${{r.plane}}</td>
        <td class="node-address">${{esc(r.address)}}</td>
        <td class="node-cell"><div class="node-name">${{esc(r.vector_name)}}</div></td>
        <td class="hitfail-${{esc(r.hit_fail)}}">${{esc(r.hit_fail)}}</td>
        <td class="quote-block">
          <span class="tag">Quote in doc${{r.is_literal_quote ? '' : ' (paraphrase)'}}</span>
          <div class="quote">${{esc(r.quote_in_doc)}}</div>
          <span class="tag">Kanon ideal (${{esc(r.address)}})</span>
          <div class="ideal">${{esc(r.og_node_ideal) || '(no Kanon ideal matched)'}}</div>
        </td>
        <td><span class="badge" style="background:${{STATUS_COLORS[r.status] || '#999'}}">${{esc(r.status)}}</span></td>
        <td class="score-cell">${{r.fuzzy_score !== null && r.fuzzy_score !== undefined ? r.fuzzy_score.toFixed(2) : '-'}}</td>
        <td class="node-address">${{r.citation_key ? '[^'+esc(r.citation_key)+']' : '(none)'}}</td>
      </tr>
    `).join('');
  }}
}}
const dash = new Dashboard(DATA);
</script>
</body>
</html>
"""
    return html_out

if __name__ == "__main__":
    rows = fetch_rows()
    out = build_html(rows)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        f.write(out)
    print(f"wrote {OUT_PATH} ({len(rows)} nodes)")
