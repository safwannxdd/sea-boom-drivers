# SEA Boom Drivers

**What has actually come before, and plausibly caused, sector booms in Southeast Asia?**

A personal research project covering all 11 SEA countries, with a focus on fintech, crypto/blockchain and other digital
sectors. The full plan is in [RESEARCH_DESIGN.md](RESEARCH_DESIGN.md).

## Status

| Phase | Status |
|---|---|
| **P0 · Data audit** | ✅ done: `notebooks/00_data_audit.ipynb` |
| **P1 · Pre-registration** | 🔒 frozen 2026-10-07: `PREREGISTRATION.md`, `drivers/events.csv` |
| **P2 · Boom catalogue** | ✅ approved: 55 series (IMF FAS, e-Conomy SEA, BNM rails, Passport food delivery, Orbis firm formation); validation 92% digital / 80% fintech; out-of-sample Passport test 83% |
| **P3 · Correlates** | ✅ approved: `03_panel_correlates`. H1 and H2 not supported (mobile-subscription takeoff hazard borderline, p = 0.053); H5 and H8 deferred |
| **P4 · Causal events** | ✅ approved: `04_causal_events`. No launch or rule shows a detectable effect (exact RI); H3 rails → mobile money +21% but p = 0.60; H5 descriptive and mixed |
| **P5 · Diffusion** | ✅ approved: `05_diffusion`. H6a uninformative, H6b significant but rests on one category (crypto), H7 not supported; mobile wallets SEA-native |
| **P6 · Validation + report** | ✅ approved: `06_validation` (RQ6 not answerable: no surviving drivers, 2 test takeoffs); final report `reports/FINAL_REPORT.md` |

### P0 result

| Sector group | Best outcome | Countries with ≥ 8 years | Verdict |
|---|---|---|---|
| Fintech | IMF FAS digital-payment value (% GDP) | 6 (ID, MY, PH, TH, VN, KH) | **GO** |
| Digital sectors | e-Conomy SEA GMV, country × sector | 0 (7 years: 2019–2025, Tier A) | **NARROW** (1 year short) |
| Crypto | regulator statistics + Chainalysis index | 0 (~2019/20–2025) | **NARROW** |

## Layout

```
drivers/config.py      countries, tiers, sectors, indicator codes
drivers/fetch.py       cached public-data fetchers  (python -m drivers.fetch <source>)
notebooks/             executed notebooks; readable sources in notebooks/_src/
data/public/           public data (raw + processed)
data/licensed/         UCL-licensed extracts: git-ignored, never shared
reports/figures/       charts
```

## Run

```bash
pip install -r requirements.txt
for s in worldbank imf_fas econsea oxcgrt coingecko; do python -m drivers.fetch $s; done
./build_notebooks.sh          # or ./build_notebooks.sh 00 for one notebook
```
