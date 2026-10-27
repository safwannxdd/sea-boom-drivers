# %% [markdown]
# # 02b · Blind Visual-Coding Sheet 2: new series (Phase P2, part 2b)
#
# Same blind design as sheet 1 (random IDs, years as Y1…Yn, values rescaled to 0–100, shuffled with a fixed seed),
# for the series added after sheet 1 was coded:
#
# | Series | Source | How the takeoff is dated |
# |---|---|---|
# | Online food ordering, 6 countries, 2020–2025 | Euromonitor Passport | **frozen** digital rule; your codes give an **out-of-sample test** |
# | New crypto / fintech firms per year (countries with ≥ 20 firms), 2005–2025 | Orbis (active firms only) | **your visual code** (unit: firms) |
#
# IDs start with **T** so they never collide with sheet 1. The key is `data/public/processed/coding_key_2.parquet`.
# Don't open it until you've finished coding.

# %%
import sys, base64, io, json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path.cwd().parent))
from drivers.config import PROC, ROOT

LIC = ROOT / "data" / "licensed" / "derived"
items = []
pp = pd.read_parquet(LIC / "passport_food_online_ordering.parquet")
for c, g in pp.groupby("iso3"):
    g = g.sort_values("year"); items.append(dict(group="digital", series="passport_food_online_ordering", iso3=c,
                                               years=g.year.tolist(), values=g.value.tolist()))
ff = pd.read_parquet(LIC / "orbis_firm_formation_PRELIMINARY.parquet")
for (kind, c), g in ff.groupby(["kind", "iso3"]):
    if g.new_firms.sum() < 20: continue
    g = g.sort_values("year"); items.append(dict(group=kind, series=f"orbis_new_{kind}_firms", iso3=c,
                                               years=g.year.tolist(), values=g.new_firms.astype(float).tolist()))
rng = np.random.default_rng(20261008)
order = rng.permutation(len(items))
ids = [f"T{n:02d}" for n in range(1, len(items) + 1)]
key2 = pd.DataFrame([dict(chart_id=ids[i], **{k: items[j][k] for k in ("group", "series", "iso3")},
                          first_year=items[j]["years"][0], n_years=len(items[j]["years"])) for i, j in enumerate(order)])
key2.to_parquet(PROC / "coding_key_2.parquet")
print(f"{len(key2)} charts:", key2.series.value_counts().to_dict())

# %%
def chart_png(values):
    v = np.array(values, float); v = 100 * v / v.max() if v.max() > 0 else v
    fig, ax = plt.subplots(figsize=(4.2, 2.4), dpi=110)
    x = np.arange(1, len(v) + 1)
    ax.plot(x, v, "-o", color="#2a78d6", lw=2, ms=4)
    ax.set_xticks(x, [f"Y{i}" for i in x], fontsize=7 if len(v) <= 12 else 6, rotation=0 if len(v) <= 12 else 90)
    ax.set_ylim(0, 105); ax.tick_params(axis="y", labelsize=8); ax.grid(alpha=.25); ax.spines[["top", "right"]].set_visible(False)
    buf = io.BytesIO(); fig.tight_layout(); fig.savefig(buf, format="png"); plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()

cards = []
for i, j in enumerate(order):
    n = len(items[j]["years"])
    opts = "".join(f'<option value="Y{k}">Y{k}</option>' for k in range(1, n + 1))
    cards.append(f'''<div class="card"><div class="id">{ids[i]}</div>
<img alt="chart {ids[i]}" src="data:image/png;base64,{chart_png(items[j]["values"])}">
<label>Takeoff year: <select id="{ids[i]}"><option value="">— choose —</option>{opts}
<option value="before">already taken off before Y1</option><option value="none">no takeoff</option></select></label></div>''')

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Takeoff Coding Sheet 2</title><style>
body{{font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;background:#f6f7f5;color:#15181d}}
header{{padding:20px 24px;background:#fff;border-bottom:1px solid #ddd;position:sticky;top:0;z-index:2}}
h1{{margin:0 0 6px;font-size:22px}} p{{margin:4px 0;max-width:75ch}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:16px;padding:20px 24px}}
.card{{background:#fff;border:1px solid #ddd;border-radius:8px;padding:10px 12px}} .card img{{width:100%}}
.id{{font-weight:700;font-family:ui-monospace,monospace}} select{{font-size:14px;margin-left:6px}}
button{{font-size:15px;padding:8px 14px;border-radius:6px;border:1px solid #1c5cab;background:#2a78d6;color:#fff;cursor:pointer}}
#status{{margin-left:12px;color:#555}}</style></head><body>
<header><h1>Takeoff coding sheet 2 ({len(ids)} charts)</h1>
<p><b>Your code marks only when a takeoff STARTED.</b> Whether it lasted or crashed is classified afterwards by separate rules.</p>
<p>• Rise lasting <b>2+ years</b>, even if it then <b>crashes</b> → mark the year the rise <b>began</b> (the crash is classified as a spike or slowdown automatically).<br>
• A <b>one-year blip</b> that falls straight back → <b>no takeoff</b>.<br>
• <b>Bumpy but trending up</b> → mark where the upward trend begins.<br>
• Already rising at Y1 → <b>already taken off before Y1</b>.</p>
<p><button onclick="dl()">Download my codes (CSV)</button><span id="status"></span></p></header>
<div class="grid">{"".join(cards)}</div>
<script>
const ids={json.dumps(ids)};
function dl(){{const rows=["chart_id,code"];let missing=0;
 for(const id of ids){{const v=document.getElementById(id).value;if(!v)missing++;rows.push(id+","+v);}}
 document.getElementById("status").textContent=missing?missing+" chart(s) not coded yet - downloaded anyway":"All coded - thank you!";
 const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([rows.join("\\n")],{{type:"text/csv"}}));
 a.download="visual_codes_2.csv";a.click();}}
</script></body></html>'''
out = ROOT / "reports" / "coding" / "takeoff_coding_sheet_2.html"
out.write_text(html); print("written:", out)
