# %% [markdown]
# # 00b · Event Timeline (Phase P1 review)
#
# A visual check of the hand-coded policy and infrastructure events in `drivers/events.csv`. These dates
# drive the causal tests (H3, H4, H9), so each one must be right **before** any outcome data is linked to it.
#
# Status legend: **verified** = two independent sources; anything else is resolved or dropped in P2.

# %%
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path.cwd().parent))
from drivers.config import ROOT, FIG, NAME, COUNTRIES

ev = pd.read_csv(ROOT / "drivers" / "events.csv", parse_dates=["date"])
print(f"{len(ev)} events across {ev.iso3.nunique()} countries")
ev.groupby(["category", "status"]).size().unstack(fill_value=0)

# %% [markdown]
# ## Timeline by country

# %%
order = [c for c in COUNTRIES if c in set(ev.iso3)]
marker = {"payment_rail": "o", "cross_border_rail": "D", "digital_bank": "s", "ride_hailing_rule": "^",
          "lending_rule": "v", "crypto_regime": "P", "ban": "X"}
color = {"verified": "#2a78d6", "verified_announcement_date": "#1baf7a", "needs_second_source": "#eda100", "needs_source": "#8a8a8a",
         "conflicting_sources": "#e34948"}
fig, ax = plt.subplots(figsize=(13, 6))
for _, r in ev.iterrows():
    y = order.index(r.iso3)
    ax.scatter(r.date, y, marker=marker[r.category], s=90, color=color[r.status], edgecolor="white", zorder=3)
    ax.annotate(r.event_id, (r.date, y), xytext=(0, 8), textcoords="offset points", ha="center", fontsize=7)
ax.set_yticks(range(len(order)), [NAME[c] for c in order])
ax.grid(axis="x", alpha=.3)
for cat, m in marker.items():
    ax.scatter([], [], marker=m, color="#444", label=cat.replace("_", " "))
for st, c in color.items():
    ax.scatter([], [], marker="o", color=c, label=st.replace("_", " "))
ax.legend(ncol=2, fontsize=8, loc="upper left")
ax.set_title("Policy & infrastructure events (shape = type, colour = verification status)")
plt.tight_layout(); plt.savefig(FIG / "00b_event_timeline.png", dpi=150); plt.show()

# %% [markdown]
# ## Events still needing work

# %%
todo = ev[ev.status != "verified"][["event_id", "iso3", "date", "category", "description", "status"]]
todo.assign(country=todo.iso3.map(NAME)).drop(columns="iso3")
