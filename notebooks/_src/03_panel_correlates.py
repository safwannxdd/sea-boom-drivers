# %% [markdown]
# # 03 · What Comes Before a Boom? Panel Correlates (Phase P3)
#
# Research question **RQ2**: which country conditions reliably *come before* growth and takeoffs in SEA digital
# markets? This tests the P3 hypotheses frozen in `PREREGISTRATION.md` §5:
#
# | # | Hypothesis | Test here |
# |---|---|---|
# | **H1** | Takeoff follows **infrastructure** (internet, mobile) more than foreign attention | panel FE on growth + discrete-time takeoff hazard |
# | **H2** | **Financial-access gaps** speed up fintech (leapfrogging) | panel FE on fintech growth with the account-ownership gap |
# | **H5** | Categories on an **anchor platform** take off faster | ⚠ not testable yet (no anchor-platform coding); see §6 |
# | **H8** | **Attention without enablers** produces spikes, not booms | ⚠ not testable yet (attention data only from 2017); see §6 |
#
# **Method (design §6.2, frozen):** two-way fixed effects (each series, each year), drivers **lagged one year**, standard
# errors clustered by country, p-values from the **wild-cluster restricted bootstrap** (Webb weights, 9,999 draws,
# because there are only 6–9 countries), **Holm** correction within each hypothesis. Two extra checks:
# **lead tests** (a future driver must not "predict" past growth) and a **placebo** (drivers shuffled across countries).
#
# **This is correlation, not causation.** Causal tests (payment-rail launches, licences) come in P4.

# %%
import sys, warnings, itertools
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

sys.path.insert(0, str(Path.cwd().parent))
from drivers.config import PROC, FIG, ROOT, NAME, COUNTRIES
from drivers import fetch
warnings.filterwarnings("ignore")
pd.set_option("display.width", 180)
RNG = np.random.default_rng(20261009)
B_DRAWS = 9999

# %% [markdown]
# ## 1 · Driver panel (country × year)
# World Bank WDI/Findex + Oxford COVID stringency. Rules:
# * **Findex account ownership** exists only in survey years (2011, 2014, 2017, 2021, 2024). It is linearly interpolated
#   between surveys and held flat after the last one. The **account gap** = 100 − ownership.
# * Values missing at the end of a series (usually 2025) carry the last value forward and are flagged.
# * All drivers are **standardised** (z-scores over the panel), so coefficients read as "effect of a one-SD difference".

# %%
wb = fetch.fetch_worldbank()
W = wb.pivot_table(index=["iso3", "year"], columns="indicator", values="value").reset_index()
full = pd.MultiIndex.from_product([list(COUNTRIES), range(2004, 2026)], names=["iso3", "year"]).to_frame(index=False)
D = full.merge(W, on=["iso3", "year"], how="left").sort_values(["iso3", "year"])
D["acct_obs"] = D.account_ownership_pct.notna()
D["account_ownership_pct"] = D.groupby("iso3").account_ownership_pct.transform(lambda s: s.interpolate(limit_area="inside"))
D["account_ownership_pct"] = D.groupby("iso3").account_ownership_pct.ffill()
D["account_gap"] = 100 - D.account_ownership_pct
for c in ["internet_users_pct", "mobile_subs_per100", "gdp_pc_ppp", "urban_pct", "remittance_inflows_pct_gdp", "private_credit_pct_gdp"]:
    D[f"{c}_filled"] = D[c].isna()
    D[c] = D.groupby("iso3")[c].ffill()
D["log_gdp_pc"] = np.log(D.gdp_pc_ppp)
ox = fetch.fetch_oxcgrt()
ox["year"] = pd.to_datetime(ox.Date.astype(str), format="%Y%m%d", errors="coerce").dt.year
st = ox.groupby(["CountryCode", "year"]).StringencyIndex_Average.mean().rename("covid_stringency").reset_index().rename(columns={"CountryCode": "iso3"})
D = D.merge(st, on=["iso3", "year"], how="left"); D["covid_stringency"] = D.covid_stringency.fillna(0)
DRIVERS = ["internet_users_pct", "mobile_subs_per100", "log_gdp_pc", "urban_pct", "account_gap",
           "remittance_inflows_pct_gdp", "private_credit_pct_gdp", "covid_stringency"]
for c in DRIVERS:
    D[c + "_z"] = (D[c] - D[c].mean()) / D[c].std()
D.to_parquet(PROC / "drivers_panel.parquet")
D[D.year.isin([2010, 2015, 2020, 2024])].pivot_table(index="iso3", columns="year", values=["internet_users_pct", "account_gap"]).round(0).rename(index=NAME)

# %% [markdown]
# ## 2 · Outcome panel for regressions (series × year)
# | Family | Outcome *y* | Why |
# |---|---|---|
# | **Fintech** (IMF FAS, % of GDP) | yearly change in asinh(value) ≈ log growth, defined at zero | pre-registered "outcome growth" |
# | **Digital** (e-Conomy GMV % GDP; Passport food delivery) | yearly change in log(value) | same |
# | **Firm formation** (Orbis new firms per million) | asinh(new firms per million), the **formation rate** | new firms are already a flow (the growth of the firm stock). Logged deviation |
#
# Malaysia's rail series (one country) can't identify cross-country effects and is left out.

# %%
P = pd.read_parquet(PROC / "outcome_panel.parquet"); P = P[~P.is_estimate]
LICD = ROOT / "data" / "licensed" / "derived"
rows = []
for (s, c), g in P[P.series.str.startswith("fas")].groupby(["series", "iso3"]):
    g = g.sort_values("year"); y = np.arcsinh(g.value.to_numpy())
    rows += [dict(family="fintech", series=s, iso3=c, year=int(t), y=d) for t, d in zip(g.year.iloc[1:], np.diff(y))]
for (s, c), g in P[P.series.str.startswith("econsea")].groupby(["series", "iso3"]):
    g = g.sort_values("year"); y = np.log(g.value.to_numpy())
    rows += [dict(family="digital", series=s, iso3=c, year=int(t), y=d) for t, d in zip(g.year.iloc[1:], np.diff(y))]
pp = pd.read_parquet(LICD / "passport_food_online_ordering.parquet")
for c, g in pp.groupby("iso3"):
    g = g.sort_values("year"); y = np.log(g.value.to_numpy())
    rows += [dict(family="digital", series="passport_food", iso3=c, year=int(t), y=d) for t, d in zip(g.year.iloc[1:], np.diff(y))]
ff = pd.read_parquet(LICD / "orbis_firm_formation_PRELIMINARY.parquet")
keep = ff.groupby(["kind", "iso3"]).new_firms.sum().loc[lambda s: s >= 20].index
for (k, c), g in ff.groupby(["kind", "iso3"]):
    if (k, c) not in keep: continue
    g = g[g.year.between(2006, 2024)]                                  # 2025 incomplete (Orbis registration lag)
    rows += [dict(family="firms", series=f"firms_{k}", iso3=c, year=int(t), y=v) for t, v in zip(g.year, np.arcsinh(g.new_per_million))]
Y = pd.DataFrame(rows)
lag = D[["iso3", "year"] + [c + "_z" for c in DRIVERS]].copy(); lag["year"] += 1           # value at t-1 aligned to t
lead = D[["iso3", "year"] + [c + "_z" for c in DRIVERS]].copy(); lead["year"] -= 1         # value at t+1 aligned to t
Y = Y.merge(lag, on=["iso3", "year"], how="left").merge(lead, on=["iso3", "year"], how="left", suffixes=("", "_lead"))
Y["sid"] = Y.series + "|" + Y.iso3
print(Y.groupby("family").agg(obs=("y", "size"), series=("sid", "nunique"), countries=("iso3", "nunique"),
                             years=("year", lambda t: f"{t.min()}–{t.max()}")))

# %% [markdown]
# ## 3 · Estimator: two-way FE + wild-cluster restricted bootstrap

# %%
WEBB = np.array([-np.sqrt(1.5), -1, -np.sqrt(0.5), np.sqrt(0.5), 1, np.sqrt(1.5)])

def design(d, xvars):
    X = pd.concat([d[xvars], pd.get_dummies(d.sid, drop_first=True, dtype=float),
                   pd.get_dummies(d.year, prefix="yr", drop_first=True, dtype=float)], axis=1)
    return sm.add_constant(X, has_constant="add").astype(float)

def cr1_t(X, y, cl, k):
    XtX_inv = np.linalg.pinv(X.T @ X); b = XtX_inv @ X.T @ y; u = y - X @ b
    G = np.unique(cl); meat = np.zeros((X.shape[1], X.shape[1]))
    for g in G:
        s = X[cl == g].T @ u[cl == g]; meat += np.outer(s, s)
    n, p = X.shape; c = len(G) / (len(G) - 1) * (n - 1) / (n - p)
    V = c * XtX_inv @ meat @ XtX_inv
    return b[k], np.sqrt(V[k, k]), b[k] / np.sqrt(V[k, k])

def wcr_pvalue(X, y, cl, k, B=B_DRAWS):
    """Wild-cluster restricted bootstrap p-value for H0: beta_k = 0 (Webb six-point weights)."""
    _, _, t_obs = cr1_t(X, y, cl, k)
    Xr = np.delete(X, k, axis=1); br = np.linalg.lstsq(Xr, y, rcond=None)[0]
    fit_r, u_r = Xr @ br, y - Xr @ br
    G, inv = np.unique(cl, return_inverse=True)
    XtX_inv = np.linalg.pinv(X.T @ X)
    n, p = X.shape; c = len(G) / (len(G) - 1) * (n - 1) / (n - p)
    t_star = np.empty(B)
    for i in range(B):
        w = RNG.choice(WEBB, size=len(G))[inv]
        ys = fit_r + w * u_r
        b = XtX_inv @ X.T @ ys; u = ys - X @ b
        meat = np.zeros((p, p))
        for g in range(len(G)):
            s = X[inv == g].T @ u[inv == g]; meat += np.outer(s, s)
        t_star[i] = b[k] / np.sqrt((c * XtX_inv @ meat @ XtX_inv)[k, k])
    return float(np.mean(np.abs(t_star) >= abs(t_obs)))

def fe_model(d, xvars, B=B_DRAWS):
    d = d.dropna(subset=["y"] + xvars)
    Xdf = design(d, xvars); X = Xdf.to_numpy(); y = d.y.to_numpy(); cl = d.iso3.to_numpy()
    out = []
    for v in xvars:
        k = list(Xdf.columns).index(v); b, se, t = cr1_t(X, y, cl, k)
        out.append(dict(driver=v.replace("_z", ""), coef=b, se=se, t=t, p_wcr=wcr_pvalue(X, y, cl, k, B)))
    return pd.DataFrame(out).assign(n=len(d), clusters=d.iso3.nunique())

# %% [markdown]
# ## 4 · H1: infrastructure → growth (all families) and → takeoff (hazard)
# Pre-registered terms: internet users and mobile subscriptions, with log GDP per capita as a control.
# **Supported if** infrastructure terms are significant (Holm-adjusted). The comparison with *foreign attention*
# cannot be run: origin-country attention data (Google Trends/GDELT) only starts in 2017, after most takeoffs.
# This is logged as a deviation, and the origin comparison moves to P5 (diffusion).

# %%
H1X = ["internet_users_pct_z", "mobile_subs_per100_z", "log_gdp_pc_z"]
h1 = pd.concat([fe_model(Y[Y.family == f], H1X).assign(family=f) for f in ["fintech", "digital", "firms"]], ignore_index=True)
def holm(p):
    p = np.asarray(p); o = np.argsort(p); m = len(p); adj = np.empty(m)
    adj[o] = np.minimum(1, np.maximum.accumulate((m - np.arange(m)) * p[o]))
    return adj
mask = h1.driver.isin(["internet_users_pct", "mobile_subs_per100"])
h1.loc[mask, "p_holm"] = holm(h1.loc[mask, "p_wcr"])
h1.round(3)

# %% [markdown]
# ### H1 hazard: what predicts the year of a dated takeoff?
# Discrete-time logit over series-years **at risk** (from the first observed year until takeoff). Series with no datable
# takeoff because they were already growing are left out (left-censored). Flat ones stay at risk throughout.
# Events come from the frozen P2 catalogue. With so few events this is **descriptive**. Odds ratios with
# country-clustered 95% CIs.

# %%
cat = pd.read_parquet(PROC / "boom_catalogue.parquet")
cat["takeoff_year"] = pd.to_numeric(cat.takeoff_year, errors="coerce")
series_years = {}
for (s, c), g in P.groupby(["series", "iso3"]): series_years[(s, c)] = sorted(g.year)
for (k, c), g in ff.groupby(["kind", "iso3"]): series_years[(f"orbis_new_{k}_firms", c)] = sorted(g.year[g.year <= 2024])
for c, g in pp.groupby("iso3"): series_years[("passport_food_online_ordering", c)] = sorted(g.year)
haz = []
for _, r in cat.iterrows():
    if "growing" in r.status or "declining" in r.status or r.series.startswith("rail"): continue
    if r.series == "econsea_online_travel": continue                          # COVID rebound, not a takeoff from zero
    yrs = series_years.get((r.series, r.iso3), [])
    for y in yrs[1:]:
        ev = int(r.takeoff_year == y) if r.takeoff_year == r.takeoff_year else 0
        haz.append(dict(series=r.series, iso3=r.iso3, year=y, event=ev))
        if ev: break
H = pd.DataFrame(haz).merge(lag, on=["iso3", "year"], how="left").dropna()
print(f"at-risk series-years: {len(H)} | takeoff events: {H.event.sum()} | series: {H.groupby(['series','iso3']).ngroups}")
Xh = sm.add_constant(H[["internet_users_pct_z", "mobile_subs_per100_z", "log_gdp_pc_z"]])
hz = sm.Logit(H.event, Xh).fit(disp=0, cov_type="cluster", cov_kwds={"groups": pd.factorize(H.iso3)[0]})
hz_tab = pd.DataFrame({"odds_ratio": np.exp(hz.params), "ci_low": np.exp(hz.conf_int()[0]),
                       "ci_high": np.exp(hz.conf_int()[1]), "p": hz.pvalues}).drop("const").round(3)
hz_tab

# %% [markdown]
# ## 5 · H2: financial-access gap → fintech growth
# Pre-registered: the account gap (100 − Findex account ownership) on fintech growth. **Supported if** the gap coefficient
# is **positive** and significant (a bigger gap means faster growth: leapfrogging). Card penetration is not in the
# public data, so it is dropped (logged). Controls: internet users and log GDP per capita.

# %%
H2X = ["account_gap_z", "internet_users_pct_z", "log_gdp_pc_z"]
h2 = fe_model(Y[Y.family == "fintech"], H2X).assign(family="fintech")
h2_firms = fe_model(Y[(Y.family == "firms") & Y.series.eq("firms_fintech")], H2X).assign(family="fintech firm formation")
h2 = pd.concat([h2, h2_firms], ignore_index=True)
m2 = h2.driver == "account_gap"; h2.loc[m2, "p_holm"] = holm(h2.loc[m2, "p_wcr"])
h2.round(3)

# %% [markdown]
# ## 6 · Robustness: lead test and placebo
# * **Lead test:** add each driver's value at *t + 1*. If future values "predict" today's growth as well as past values
#   do, the correlation reflects shared trends or reverse causality, not drivers running ahead of booms.
# * **Placebo:** reassign each country's whole driver history to a random other country (999 permutations) and re-estimate.
#   The real coefficient should be extreme relative to this background.

# %%
def lead_test(d, var):
    xv = [var + "_z", var + "_z_lead", "log_gdp_pc_z"]
    d = d.dropna(subset=["y"] + xv)
    Xdf = design(d, xv); X = Xdf.to_numpy(); y = d.y.to_numpy(); cl = d.iso3.to_numpy()
    res = {}
    for v in [var + "_z", var + "_z_lead"]:
        k = list(Xdf.columns).index(v); b, se, t = cr1_t(X, y, cl, k)
        res[v] = (round(b, 3), round(wcr_pvalue(X, y, cl, k, 1999), 3))
    return res

lead_rows = []
for fam, var in [("fintech", "internet_users_pct"), ("fintech", "account_gap"), ("digital", "internet_users_pct"),
                 ("firms", "internet_users_pct")]:
    r = lead_test(Y[Y.family == fam], var)
    lead_rows.append(dict(family=fam, driver=var, lag_coef_p=r[var + "_z"], lead_coef_p=r[var + "_z_lead"]))
pd.DataFrame(lead_rows)

# %%
def placebo(d, xvars, target, n=999):
    real = fe_model(d, xvars, B=99).set_index("driver").coef[target.replace("_z", "")]
    ctry = d.iso3.unique(); vals = []
    Dz = D.set_index(["iso3", "year"])[[c for c in xvars]]
    for _ in range(n):
        perm = dict(zip(ctry, RNG.permutation(ctry)))
        dd = d.copy()
        src = pd.MultiIndex.from_arrays([dd.iso3.map(perm), dd.year - 1])
        dd[xvars] = Dz.reindex(src).to_numpy()
        dd = dd.dropna(subset=["y"] + xvars)
        Xdf = design(dd, xvars); X = Xdf.to_numpy()
        b = np.linalg.lstsq(X, dd.y.to_numpy(), rcond=None)[0]
        vals.append(b[list(Xdf.columns).index(target)])
    vals = np.array(vals)
    return real, float(np.mean(np.abs(vals) >= abs(real)))

plac = []
for fam, xv, tgt in [("fintech", H1X, "internet_users_pct_z"), ("digital", H1X, "internet_users_pct_z"),
                     ("firms", H1X, "internet_users_pct_z"), ("fintech", H2X, "account_gap_z")]:
    real, p = placebo(Y[Y.family == fam], xv, tgt)
    plac.append(dict(family=fam, driver=tgt.replace("_z", ""), real_coef=round(real, 3), placebo_p=round(p, 3)))
pd.DataFrame(plac)

# %% [markdown]
# ## 7 · H5 and H8: why they are not tested yet
# * **H5 (anchor platforms)** needs a hand-coded table of when a super-app (Grab, Gojek, Shopee, etc.) began distributing
#   each category in each country, with two sources per date (pre-registration §6). That table does not exist yet.
# * **H8 (attention × enablers)** needs news or search attention at each takeoff. GDELT starts in 2017 and Google
#   Trends rate-limits this connection. Of the dated takeoffs, too few fall after 2017 for a spike-vs-boom model.
#
# Both are logged as deviations and carried forward. H5 can be coded alongside the P4 event work.

# %% [markdown]
# ## 8 · Results summary
# | Hypothesis | Result | Verdict |
# |---|---|---|
# | **H1 growth** (infrastructure → growth) | Internet-user coefficients are **negative** in all three families (fintech −0.52, firms −0.40, digital −0.14 per SD); none significant after the wild-cluster bootstrap (p 0.18–0.54; Holm 1.0) | **Not supported** |
# | **H1 hazard** (infrastructure → takeoff timing) | 12 takeoffs in 100 at-risk years. Mobile subscriptions: odds ratio **2.2** per SD (95% CI 0.99–5.0, p = 0.053); internet: 0.86 (p = 0.70) | **Not supported** at α = 0.05; mobile is borderline |
# | **H2** (account gap → fintech growth) | Gap coefficient **−0.35** (wrong sign for leapfrogging), p = 0.21, Holm 0.42; zero for fintech firm formation | **Not supported** |
# | **H5** (anchor platforms) | Not run: no anchor-platform coding yet | **Deferred** |
# | **H8** (attention × enablers) | Not run: attention data starts in 2017 | **Deferred** |
# | Lead test | Future drivers are no weaker than past ones (all n.s.) | Consistent with no driver-ahead-of-boom signal |
# | Placebo | Real coefficients are not extreme against shuffled countries (p 0.09–0.43) | Background-level correlation |
#
# **How to read the negative internet coefficients:** they are what an **S-curve** produces. Growth is fastest when
# penetration is low and slows as markets saturate. Within a country, higher internet use coincides with *slower*
# growth of an already-adopted category. This is a growth-rate (diffusion) effect, not evidence that internet access
# hurts booms. The hazard model asks the right question for H1 (does infrastructure come *before* takeoff?), and there
# the mobile-subscription signal is the strongest in P3, at p = 0.053.
#
# **Power:** 6–7 country clusters and 12 dated takeoffs. These tests can detect only large effects, so "not supported"
# means "no large, robust effect", not "no effect". P4's event studies use within-country timing shocks (payment-rail
# launches, licences) and are better placed to find causal effects with this few countries.
