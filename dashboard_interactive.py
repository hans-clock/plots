import pandas as pd
import numpy as np
from IPython.display import display, HTML
import json

# ── DATA ─────────────────────────────────────────────────────────────────────
np.random.seed(42)
n = 120
df = pd.DataFrame({
    'Country':  np.random.choice(['Netherlands', 'Germany', 'Belgium', 'France'], n),
    'Region':   np.random.choice(['North', 'South', 'East', 'West'], n),
    'Type':     np.random.choice(['Jackets', 'Trousers', 'Shirts', 'Shoes'], n),
    'Date':     pd.date_range('2024-01-01', periods=n, freq='3D'),
    'Quantity': np.random.randint(10, 300, n),
    'Price':    np.random.choice([29.99, 49.99, 79.99, 99.99], n),
})
df['Date'] = df['Date'].dt.strftime('%Y-%m')
df = df.reset_index(drop=True)

records = df.to_dict(orient='records')

display(HTML(f"""
<div id="wif-root">

<style>
  #wif-root {{ font-family: sans-serif; font-size: 13px; }}
  .wif-filters {{ display:flex; gap:12px; align-items:flex-start; margin-bottom:12px; flex-wrap:wrap; }}
  .wif-filters label {{ font-size:11px; color:#555; display:block; margin-bottom:3px; text-transform:uppercase; letter-spacing:.05em }}
  .wif-filters select {{ height:100px; width:150px; font-size:12px; border:1px solid #ccc; border-radius:4px; padding:2px; }}
  .wif-btn {{ padding:7px 16px; border:none; border-radius:4px; cursor:pointer; font-size:12px; font-weight:600; }}
  .wif-btn-apply {{ background:#1565c0; color:white; }}
  .wif-btn-reset {{ background:#f59e0b; color:white; }}
  .wif-totals {{ display:flex; gap:12px; margin:12px 0; }}
  .wif-card {{ flex:1; padding:14px 18px; border-radius:8px; }}
  .wif-card-blue {{ background:#e3f2fd; border:1px solid #90caf9; }}
  .wif-card-green {{ background:#e8f5e9; border:1px solid #a5d6a7; }}
  .wif-card-title {{ font-size:10px; color:#555; text-transform:uppercase; letter-spacing:.05em; margin-bottom:6px; }}
  .wif-card-nums {{ display:flex; gap:20px; align-items:baseline; }}
  .wif-num-label {{ font-size:10px; color:#888; }}
  .wif-num-val {{ font-size:22px; font-weight:700; }}
  .wif-table-wrap {{ max-height:420px; overflow-y:auto; border:1px solid #ddd; border-radius:6px; }}
  table {{ border-collapse:collapse; width:100%; }}
  thead tr {{ background:#1565c0; color:white; position:sticky; top:0; }}
  th {{ padding:8px 10px; text-align:left; font-size:12px; white-space:nowrap; }}
  th.num {{ text-align:right; }}
  tbody tr:nth-child(even) {{ background:#f5f5f5; }}
  tbody tr.edited {{ background:#fffbe6; }}
  td {{ padding:5px 10px; white-space:nowrap; }}
  td.num {{ text-align:right; }}
  .qty-input {{ width:72px; padding:3px 5px; border:1px solid #bbb; border-radius:3px; font-size:12px; text-align:right; }}
  .qty-input:focus {{ outline:2px solid #1565c0; }}
  .pos {{ color:#2e7d32; font-weight:700; }}
  .neg {{ color:#c62828; font-weight:700; }}
  #wif-chart-wrap {{
    margin-top:28px; padding:20px;
    border:1px solid #ddd; border-radius:8px; background:#fafafa;
  }}
  #wif-chart-title {{
    font-size:13px; font-weight:600; color:#333; margin-bottom:16px;
  }}
  #wif-canvas {{ width:100%; height:260px; display:block; }}
</style>

<div class="wif-filters">
  <div><label>Country</label><select id="f-country" multiple></select></div>
  <div><label>Region</label><select id="f-region" multiple></select></div>
  <div><label>Type</label><select id="f-type" multiple></select></div>
  <div><label>Date</label><select id="f-date" multiple></select></div>
  <div style="display:flex;flex-direction:column;gap:6px;justify-content:flex-end;padding-bottom:2px">
    <button class="wif-btn wif-btn-apply" onclick="applyFilters()">Apply Filters</button>
    <button class="wif-btn wif-btn-reset" onclick="resetAll()">Reset All</button>
  </div>
</div>

<div class="wif-totals">
  <div class="wif-card wif-card-blue">
    <div class="wif-card-title">Total Quantity</div>
    <div class="wif-card-nums">
      <div><div class="wif-num-label">Original</div><div class="wif-num-val" id="t-orig-qty">—</div></div>
      <div style="font-size:18px;color:#aaa">→</div>
      <div><div class="wif-num-label">What-If</div><div class="wif-num-val" id="t-wi-qty">—</div></div>
      <div><div class="wif-num-label">Delta</div><div class="wif-num-val" id="t-dq">—</div></div>
    </div>
  </div>
  <div class="wif-card wif-card-green">
    <div class="wif-card-title">Total Revenue</div>
    <div class="wif-card-nums">
      <div><div class="wif-num-label">Original</div><div class="wif-num-val" id="t-orig-rev">—</div></div>
      <div style="font-size:18px;color:#aaa">→</div>
      <div><div class="wif-num-label">What-If</div><div class="wif-num-val" id="t-wi-rev">—</div></div>
      <div><div class="wif-num-label">Delta</div><div class="wif-num-val" id="t-dr">—</div></div>
    </div>
  </div>
</div>

<div id="wif-info" style="font-size:12px;color:#666;margin-bottom:4px"></div>
<div class="wif-table-wrap">
  <table>
    <thead>
      <tr>
        <th>Country</th><th>Region</th><th>Type</th><th>Date</th>
        <th class="num">Orig Qty</th>
        <th style="text-align:center">What-If Qty</th>
        <th class="num">Orig Rev</th>
        <th class="num">What-If Rev</th>
      </tr>
    </thead>
    <tbody id="wif-tbody"></tbody>
  </table>
</div>

<!-- ── CHART ── -->
<div id="wif-chart-wrap">
  <div id="wif-chart-title">Revenue over Time — Original vs What-If</div>
  <canvas id="wif-canvas"></canvas>
</div>

</div>

<script>
(function() {{
  const ALL_DATA = {json.dumps(records)};
  const edits = {{}};
  let filtered = [...ALL_DATA];

  function uniqueVals(col) {{
    return [...new Set(ALL_DATA.map(r => r[col]))].sort();
  }}
  function populateSelect(id, col) {{
    const sel = document.getElementById(id);
    sel.innerHTML = '<option value="__ALL__" selected>— All —</option>';
    uniqueVals(col).forEach(v => {{
      const o = document.createElement('option');
      o.value = v; o.textContent = v; sel.appendChild(o);
    }});
  }}
  populateSelect('f-country', 'Country');
  populateSelect('f-region',  'Region');
  populateSelect('f-date',    'Date');
  populateSelect('f-type',    'Type');

  function getSelected(id) {{
    const vals = [...document.getElementById(id).selectedOptions].map(o => o.value);
    return vals.includes('__ALL__') ? null : vals;
  }}

  window.applyFilters = function() {{
    const country = getSelected('f-country');
    const region  = getSelected('f-region');
    const type    = getSelected('f-type');
    const date    = getSelected('f-date');
    filtered = ALL_DATA.filter(r =>
      (!country || country.includes(r.Country)) &&
      (!region  || region.includes(r.Region))   &&
      (!type    || type.includes(r.Type))        &&
      (!date    || date.includes(r.Date))
    );
    Object.keys(edits).forEach(k => delete edits[k]);
    renderTable();
    updateTotals();
    renderChart();
  }};

  window.resetAll = function() {{
    ['f-country','f-region','f-type','f-date'].forEach(id => {{
      const sel = document.getElementById(id);
      [...sel.options].forEach(o => o.selected = o.value === '__ALL__');
    }});
    applyFilters();
  }};

  // ── totals ────────────────────────────────────────────────────────────────
  function fmt(n)  {{ return n.toLocaleString('en', {{maximumFractionDigits:0}}); }}
  function fmtE(n) {{ return '€' + fmt(n); }}
  function fmtD(n) {{ return (n >= 0 ? '+' : '') + fmt(n); }}
  function fmtP(n) {{ return '(' + (n >= 0 ? '+' : '') + n.toFixed(1) + '%)'; }}
  function colorCls(v) {{ return v > 0 ? 'pos' : v < 0 ? 'neg' : ''; }}

  function updateTotals() {{
    let origQty=0, wiQty=0, origRev=0, wiRev=0;
    filtered.forEach((r,i) => {{
      const wq = edits[i] !== undefined ? edits[i] : r.Quantity;
      origQty += r.Quantity;  wiQty  += wq;
      origRev += r.Quantity * r.Price;
      wiRev   += wq * r.Price;
    }});
    const dq = wiQty - origQty, dr = wiRev - origRev;
    const pq = origQty ? dq/origQty*100 : 0;
    const pr = origRev ? dr/origRev*100 : 0;

    document.getElementById('t-orig-qty').textContent = fmt(origQty);
    document.getElementById('t-wi-qty').textContent   = fmt(wiQty);
    document.getElementById('t-orig-rev').textContent = fmtE(origRev);
    document.getElementById('t-wi-rev').textContent   = fmtE(wiRev);

    const dqEl = document.getElementById('t-dq');
    dqEl.textContent = fmtD(dq) + ' ' + fmtP(pq);
    dqEl.className   = 'wif-num-val ' + colorCls(dq);

    const drEl = document.getElementById('t-dr');
    drEl.textContent = (dr>=0?'+€':'−€') + fmt(Math.abs(dr)) + ' ' + fmtP(pr);
    drEl.className   = 'wif-num-val ' + colorCls(dr);
  }}

  // ── table ─────────────────────────────────────────────────────────────────
  function renderTable() {{
    const tbody = document.getElementById('wif-tbody');
    document.getElementById('wif-info').textContent =
      filtered.length + ' rows shown — edit What-If Qty, totals update instantly.';
    tbody.innerHTML = '';
    filtered.forEach((r, i) => {{
      const wq      = edits[i] !== undefined ? edits[i] : r.Quantity;
      const origRev = r.Quantity * r.Price;
      const wiRev   = wq * r.Price;
      const edited  = edits[i] !== undefined;
      const tr      = document.createElement('tr');
      if (edited) tr.classList.add('edited');
      tr.innerHTML = `
        <td>${{r.Country}}</td><td>${{r.Region}}</td>
        <td>${{r.Type}}</td><td>${{r.Date}}</td>
        <td class="num">${{fmt(r.Quantity)}}</td>
        <td style="text-align:center">
          <input class="qty-input" type="number" min="0" value="${{wq}}"
                 data-idx="${{i}}" data-price="${{r.Price}}">
        </td>
        <td class="num">${{fmtE(origRev)}}</td>
        <td class="num" id="wirev-${{i}}">${{fmtE(wiRev)}}</td>`;
      tbody.appendChild(tr);
    }});

    tbody.querySelectorAll('.qty-input').forEach(inp => {{
      inp.addEventListener('input', function() {{
        const i     = parseInt(this.dataset.idx);
        const price = parseFloat(this.dataset.price);
        const newQ  = parseInt(this.value) || 0;
        edits[i]    = newQ;

        const origRev = filtered[i].Quantity * price;
        const wiRev   = newQ * price;
        const revEl   = document.getElementById('wirev-' + i);
        revEl.textContent = fmtE(wiRev);
        revEl.className   = 'num ' + colorCls(wiRev - origRev);
        this.closest('tr').classList.add('edited');

        updateTotals();
        renderChart();   // ← update chart on every edit
      }});
    }});
  }}

  // ── chart ─────────────────────────────────────────────────────────────────
  // aggregate filtered rows by Date, compute orig + whatif revenue per month
  function buildChartData() {{
    const origByDate = {{}};
    const wiByDate   = {{}};
    filtered.forEach((r, i) => {{
      const wq = edits[i] !== undefined ? edits[i] : r.Quantity;
      origByDate[r.Date] = (origByDate[r.Date] || 0) + r.Quantity * r.Price;
      wiByDate[r.Date]   = (wiByDate[r.Date]   || 0) + wq          * r.Price;
    }});
    const labels = Object.keys(origByDate).sort();
    return {{
      labels,
      orig: labels.map(d => origByDate[d]),
      wi:   labels.map(d => wiByDate[d]),
    }};
  }}

  let chartCtx = null;

  function renderChart() {{
    const {{ labels, orig, wi }} = buildChartData();
    const canvas = document.getElementById('wif-canvas');
    const W = canvas.offsetWidth || 800;
    const H = 260;
    canvas.width  = W;
    canvas.height = H;
    const ctx = canvas.getContext('2d');
    ctx.clearRect(0, 0, W, H);

    if (!labels.length) return;

    const pad = {{ top:20, right:20, bottom:40, left:72 }};
    const cw  = W - pad.left - pad.right;
    const ch  = H - pad.top  - pad.bottom;

    const allVals = [...orig, ...wi];
    const maxV = Math.max(...allVals) * 1.08;
    const minV = Math.min(...allVals, 0);
    const range = maxV - minV || 1;

    function xPos(i)  {{ return pad.left + (i / (labels.length - 1 || 1)) * cw; }}
    function yPos(v)  {{ return pad.top  + ch - ((v - minV) / range) * ch; }}

    // ── grid lines ────────────────────────────────────────────────────────
    ctx.strokeStyle = '#e5e7eb';
    ctx.lineWidth   = 1;
    const ticks = 5;
    for (let t = 0; t <= ticks; t++) {{
      const v = minV + (range / ticks) * t;
      const y = yPos(v);
      ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(pad.left + cw, y); ctx.stroke();
      ctx.fillStyle   = '#9ca3af';
      ctx.font        = '11px sans-serif';
      ctx.textAlign   = 'right';
      ctx.fillText('€' + fmt(v), pad.left - 6, y + 4);
    }}

    // ── x labels ──────────────────────────────────────────────────────────
    ctx.fillStyle  = '#6b7280';
    ctx.font       = '11px sans-serif';
    ctx.textAlign  = 'center';
    const step = Math.ceil(labels.length / 12);   // max ~12 labels
    labels.forEach((lbl, i) => {{
      if (i % step !== 0 && i !== labels.length - 1) return;
      ctx.fillText(lbl, xPos(i), H - pad.bottom + 18);
    }});

    // ── draw line ─────────────────────────────────────────────────────────
    function drawLine(vals, color, dash) {{
      ctx.beginPath();
      ctx.strokeStyle = color;
      ctx.lineWidth   = 2.5;
      ctx.setLineDash(dash || []);
      vals.forEach((v, i) => {{
        i === 0 ? ctx.moveTo(xPos(i), yPos(v)) : ctx.lineTo(xPos(i), yPos(v));
      }});
      ctx.stroke();
      ctx.setLineDash([]);
      // dots
      ctx.fillStyle = color;
      vals.forEach((v, i) => {{
        ctx.beginPath();
        ctx.arc(xPos(i), yPos(v), 3.5, 0, Math.PI*2);
        ctx.fill();
      }});
    }}

    drawLine(orig, '#1565c0');
    drawLine(wi,   '#e53935', [6, 3]);

    // ── legend ────────────────────────────────────────────────────────────
    const lx = pad.left + cw - 180, ly = pad.top + 10;
    [[  '#1565c0', [], 'Original Revenue'  ],
     [  '#e53935', [6,3], 'What-If Revenue']].forEach(([col, dash, label], idx) => {{
      const y = ly + idx * 20;
      ctx.strokeStyle = col; ctx.lineWidth = 2.5;
      ctx.setLineDash(dash);
      ctx.beginPath(); ctx.moveTo(lx, y); ctx.lineTo(lx + 24, y); ctx.stroke();
      ctx.setLineDash([]);
      ctx.fillStyle = col; ctx.beginPath();
      ctx.arc(lx + 12, y, 3.5, 0, Math.PI*2); ctx.fill();
      ctx.fillStyle = '#374151'; ctx.font = '11px sans-serif'; ctx.textAlign = 'left';
      ctx.fillText(label, lx + 30, y + 4);
    }});
  }}

  // init
  renderTable();
  updateTotals();
  renderChart();

  // redraw chart if canvas resizes
  window.addEventListener('resize', renderChart);
}})();
</script>
"""))
