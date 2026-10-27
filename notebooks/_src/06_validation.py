# %% [markdown]
# # 06 · Out-of-Sample Validation (Phase P6, RQ6)
#
# **Pre-registered test (PREREGISTRATION.md §7):** using only drivers that survived P3–P4, train on takeoffs resolved by
# end-2020 and predict takeoffs in **2021–2025**. Metric: AUC with bootstrap CI. Benchmarks: "follow the attention" and
# the SF-signal radar.
#
# **What can and can't be done, stated up front:**
# * **No driver survived P3–P4.** The pre-registered drivers model therefore has no inputs: it is the base rate, AUC = 0.5
#   by construction.
# * **Test set:** 9 series at risk of takeoff from 2021 (not already growing through the window), and **2** dated takeoffs
#   (Malaysia e-money 2021, Thailand fintech firm formation 2022). Any AUC on two positives is essentially uninformative.
# * **"Follow the attention" benchmark:** not runnable (no pre-2021 attention data per series).
# * **SF-radar benchmark:** the radar scores *sectors*, not SEA countries, so it can't rank these series.
#
# The notebook runs the test anyway, so the record is complete, plus one **exploratory** check (not pre-registered)
# using P3's strongest borderline signal.

# %%
import sys, warnings
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score

sys.path.insert(0, str(Path.cwd().parent))
from drivers.config import PROC, NAME
warnings.filterwarnings("ignore")

cat = pd.read_parquet(PROC / "boom_catalogue.parquet")
cat["takeoff_year"] = pd.to_numeric(cat.takeoff_year, errors="coerce")
cat = cat[cat.series != "econsea_online_travel"]                     # COVID rebound (as in P3–P5)
train = cat[cat.takeoff_year <= 2020]
test = cat[(cat.takeoff_year.isna() | (cat.takeoff_year >= 2021)) & (cat.last_year >= 2022)
           & ~cat.status.str.contains("growing|declining")].copy()
test["y"] = test.takeoff_year.between(2021, 2025).astype(int)
print(f"training takeoffs (≤2020): {len(train)} | test series: {len(test)} | test takeoffs: {test.y.sum()}")
test[["series", "country", "status", "y"]]

# %% [markdown]
# ## 1 · Pre-registered model: drivers that survived P3–P4 (none) → base rate

# %%
test["p_drivers_model"] = train.shape[0] / max(len(cat), 1)                 # constant: no surviving drivers
print("AUC, pre-registered drivers model:", roc_auc_score(test.y, test.p_drivers_model), "(constant prediction)")

# %% [markdown]
# ## 2 · Exploratory (not pre-registered): mobile subscriptions in 2020
# P3's strongest signal was the takeoff hazard for mobile subscriptions (odds ratio 2.2, p = 0.053), which did not pass.
# Here, the at-risk series are ranked by their country's 2020 mobile-subscription level, only to see which way it points.

# %%
D = pd.read_parquet(PROC / "drivers_panel.parquet")
mob = D[D.year == 2020].set_index("iso3").mobile_subs_per100
test["mobile_subs_2020"] = test.iso3.map(mob)
auc = roc_auc_score(test.y, test.mobile_subs_2020)
boot = []
rng = np.random.default_rng(2026)
for _ in range(5000):
    s = test.sample(len(test), replace=True, random_state=int(rng.integers(1e9)))
    if s.y.nunique() == 2: boot.append(roc_auc_score(s.y, s.mobile_subs_2020))
print(f"exploratory AUC = {auc:.2f}, bootstrap 95% CI {np.percentile(boot, 2.5):.2f}–{np.percentile(boot, 97.5):.2f} (2 positives)")
test[["series", "country", "mobile_subs_2020", "y"]].sort_values("mobile_subs_2020", ascending=False)

# %% [markdown]
# ## 3 · Verdict
# RQ6 **cannot be answered** with the public data assembled here. The pre-registered model is empty because nothing
# survived P3–P4, and the test window holds two takeoffs. This is not a failed prediction. It is a test that needs
# more data: more countries (South Asia, Latin America as comparison groups), more dated takeoffs (monthly central-bank
# series, deal data), or a longer window (re-run in 2028–2030 against today's frozen catalogue).
