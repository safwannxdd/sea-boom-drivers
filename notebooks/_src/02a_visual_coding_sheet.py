# %% [markdown]
# # 02a · Blind Visual-Coding Sheet (Phase P2, part 2)
#
# The pre-registration (§2.1) copies the method of Tellis, Stremersch & Yin (2003): a person marks takeoff
# years **by eye**, the threshold rule is fitted to those marks on a random half of the series, and it is
# validated on the other half.
#
# This notebook builds the marking sheet so that the coder cannot recognise any series:
# * every chart gets a **random ID**; country, sector and source are hidden
# * years are shown as **Y1…Yn**, so COVID-year dips can't give the period away
# * values are rescaled to **0–100** (each series' own maximum = 100)
# * chart order is shuffled with a fixed seed
#
# The key linking IDs to series is written to `data/public/processed/coding_key.parquet`.
# **The coder should not open it until coding is finished.**
#
# **Which series are coded:** every outcome series in the panel with **≥ 5 actual years**. Estimates are excluded,
# as the pre-registration requires, which drops the 2025 e-Conomy H1-annualised figures. Every series is coded,
# not only the calibration half, because validation also compares the rule against the visual codes.
#
# **Answer options per chart:** a year **Y1…Yn**; **"before"** = it had already taken off when the data starts
# (left-censored, added to the pre-registered options because e-Conomy data only starts in 2019); or
# **"none"** = no takeoff visible.

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

P = pd.read_parquet(PROC / "outcome_panel.parquet")
P = P[~P.is_estimate]
series = (P.groupby(["group", "series", "iso3"])
            .filter(lambda g: g.year.nunique() >= 5)
            .groupby(["group", "series", "iso3"]))
items = []
for (grp, s, c), g in series:
    g = g.sort_values("year")
    items.append(dict(group=grp, series=s, iso3=c, years=g.year.tolist(), values=g.value.tolist()))
rng = np.random.default_rng(20261007)                         # fixed seed, recorded in the pre-registration log
order = rng.permutation(len(items))
ids = [f"S{n:02d}" for n in range(1, len(items) + 1)]
key = pd.DataFrame([dict(chart_id=ids[i], **{k: items[j][k] for k in ("group", "series", "iso3")},
                         first_year=items[j]["years"][0], n_years=len(items[j]["years"]))
                    for i, j in enumerate(order)])
# calibration / validation split, stratified by sector group (pre-registration §2.1)
key["half"] = ""
for grp, idx in key.groupby("group").groups.items():
    idx = list(idx); rng.shuffle(idx)
    key.loc[idx[: len(idx) // 2 + len(idx) % 2], "half"] = "calibration"
    key.loc[idx[len(idx) // 2 + len(idx) % 2:], "half"] = "validation"
key.to_parquet(PROC / "coding_key.parquet")
print(f"{len(key)} series to code:", key.group.value_counts().to_dict())
print("split:", key.groupby(["group", "half"]).size().unstack().to_dict())

# %% [markdown]
# ## Build the HTML sheet

# %%
def chart_png(values):
    v = np.array(values, float); v = 100 * v / v.max() if v.max() > 0 else v
    fig, ax = plt.subplots(figsize=(4.2, 2.4), dpi=110)
    x = np.arange(1, len(v) + 1)
    ax.plot(x, v, "-o", color="#2a78d6", lw=2, ms=4)
    ax.set_xticks(x, [f"Y{i}" for i in x], fontsize=7 if len(v) <= 12 else 6, rotation=0 if len(v) <= 12 else 90); ax.set_ylim(0, 105); ax.tick_params(axis="y", labelsize=8)
    ax.grid(alpha=.25); ax.spines[["top", "right"]].set_visible(False)
    buf = io.BytesIO(); fig.tight_layout(); fig.savefig(buf, format="png"); plt.close(fig)
    return base64.b64encode(buf.getvalue()).decode()

cards = []
for i, j in enumerate(order):
    it = items[j]; n = len(it["years"])
    opts = "".join(f'<option value="Y{k}">Y{k}</option>' for k in range(1, n + 1))
    cards.append(f'''<div class="card"><div class="id">{ids[i]}</div>
<img alt="chart {ids[i]}" src="data:image/png;base64,{chart_png(it["values"])}">
<label>Takeoff year: <select id="{ids[i]}"><option value="">— choose —</option>{opts}
<option value="before">already taken off before Y1</option><option value="none">no takeoff</option></select></label></div>''')

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Takeoff Coding Sheet</title><style>
body{{font:15px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;margin:0;background:#f6f7f5;color:#15181d}}
header{{padding:20px 24px;background:#fff;border-bottom:1px solid #ddd;position:sticky;top:0;z-index:2}}
h1{{margin:0 0 6px;font-size:22px}} p{{margin:4px 0;max-width:75ch}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:16px;padding:20px 24px}}
.card{{background:#fff;border:1px solid #ddd;border-radius:8px;padding:10px 12px}} .card img{{width:100%}}
.id{{font-weight:700;font-family:ui-monospace,monospace}} select{{font-size:14px;margin-left:6px}}
button{{font-size:15px;padding:8px 14px;border-radius:6px;border:1px solid #1c5cab;background:#2a78d6;color:#fff;cursor:pointer}}
#status{{margin-left:12px;color:#555}}</style></head><body>
<header><h1>Takeoff coding sheet ({len(ids)} charts)</h1>
<p><b>Takeoff</b> = the first year of a dramatic, sustained increase: the start of the growth phase, not just any rise.
Mark the year where the curve "breaks upward" and keeps going.</p>
<p>Choose <b>already taken off before Y1</b> if it is clearly growing fast from the first point, and <b>no takeoff</b> if there is no clear break.
Values are rescaled to 0–100 and the years are anonymised, so judge the shape only. Don't overthink each one; about 30 seconds per chart.</p>
<p><button onclick="dl()">Download my codes (CSV)</button><span id="status"></span></p></header>
<div class="grid">{"".join(cards)}</div>
<script>
const ids={json.dumps(ids)};
function dl(){{const rows=["chart_id,code"];let missing=0;
 for(const id of ids){{const v=document.getElementById(id).value;if(!v)missing++;rows.push(id+","+v);}}
 document.getElementById("status").textContent=missing?missing+" chart(s) not coded yet - downloaded anyway":"All coded - thank you!";
 const a=document.createElement("a");a.href=URL.createObjectURL(new Blob([rows.join("\\n")],{{type:"text/csv"}}));
 a.download="visual_codes.csv";a.click();}}
</script></body></html>'''
out = ROOT / "reports" / "coding" / "takeoff_coding_sheet.html"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(html)
print("written:", out)
