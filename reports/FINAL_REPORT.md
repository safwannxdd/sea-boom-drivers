# What Makes a Sector Boom in Southeast Asia?

**Final report · personal research project · October 2026**

---

## Summary

This project asked what comes before, and plausibly causes, sector booms in Southeast Asia's digital economy,
with a focus on fintech and crypto/blockchain. It built a dated catalogue of 55 country-level series, then tested nine
pre-registered hypotheses about infrastructure, financial-access gaps, payment-system launches, licensing, super-apps,
hype, and where booms come from.

**Headline: with public and university-licensed data, no country condition, policy event or origin pattern showed a
robust effect on when or whether SEA sectors boom.** That is a finding about the limits of what 6–11 countries and
about a decade of data can reveal. It is not proof that these factors don't matter.

What the project does establish:

1. **A validated, dated boom catalogue.** A takeoff rule calibrated against blind visual coding (agreement 92% for digital,
   80% for fintech, 83% on an out-of-sample food-delivery check) identifies 11 booms, 10 spikes and 34 series with no
   datable takeoff.
2. **Most digital sectors took off before 2019.** E-commerce, online media and transport & food were already growing when
   the e-Conomy SEA series begin, so their takeoffs can't be dated from public data.
3. **Smaller markets took off first.** Cambodia led mobile money (2011) and fintech firm formation (2014), Vietnam led
   crypto firm formation (2014), and Malaysia led fintech firm formation (2014, alongside Cambodia).
4. **Mobile wallets are SEA-native.** The Philippines' GCash launched in 2004, the same year as China's Alipay and years
   before the US and India.
5. **Crypto firm formation follows the global cycle.** Every country's formation spiked in 2017–18 and 2021–22, whatever
   its regulation.
6. **Food delivery peaked in 2021.** Separated from ride-hailing (Euromonitor), online food ordering fell back after 2021 in
   the Philippines, Singapore and Indonesia, which the combined e-Conomy figure hides.
7. **The most promising lead:** national payment systems were followed by about +21% mobile-money growth, with no
   pre-trend, but this is not significant with 8 countries.

---

## 1 · Why this question

An earlier study (the SF radar) assumed SEA booms start as San Francisco trends. It found that assumption weak: the
SF→SEA link was real but tighter for hype than for booms. This project reverses the direction. It starts from booms
measured inside SEA and asks what preceded them, wherever the idea came from.

## 2 · Data

| Group | Outcome | Source | Coverage |
|---|---|---|---|
| Fintech | Mobile-money and mobile/internet-banking transaction value, % GDP | IMF Financial Access Survey | 8 countries, 2004–2025 |
| Fintech (rails) | DuitNow / e-money transactions per adult | Bank Negara Malaysia | Malaysia, 2019–2025 |
| Digital | GMV by sector, % GDP, chain-linked across 30 country reports | e-Conomy SEA (Google, Temasek, Bain) | 6 countries, 2019–2024 |
| Digital | Online food ordering, % GDP | Euromonitor Passport (UCL) | 6 countries, 2020–2025 |
| Crypto / fintech | New firms per year by incorporation date | Orbis (UCL), active firms only | 7 countries, 2005–2025 |
| Drivers | Internet, mobile, income, urbanisation, Findex accounts, remittances, credit, COVID stringency | World Bank, Oxford OxCGRT | 11 countries |
| Events | 39 payment-rail, licensing, ride-hailing, crypto and ban events (36 two-source verified) | regulators, central banks, press | `drivers/events.csv` |
| Super-apps | Anchor-wallet launch years | company and press sources | `drivers/anchors.csv` |
| Diffusion | First scaled launch per category × country (6 × 9) | company and press sources | `drivers/launches.csv` |

## 3 · Method

* **Pre-registration.** Boom definitions, hypotheses and tests were frozen before outcome data were linked to drivers
  (`PREREGISTRATION.md`). **29 deviations** are logged with dates and reasons. The most important: one permitted
  revision of the takeoff coding, and the switch from takeoff dates to launch dates for diffusion.
* **Takeoff rule.** Following Golder & Tellis (1997) and Tellis, Stremersch & Yin (2003): growth must exceed a threshold
  that falls as the base grows. As in those papers, the threshold was **calibrated to blind visual coding** (anonymised
  charts) on half the series and validated on the other half.
* **Slowdown rule.** Growth ends at the first year after takeoff that is followed by two lower years (Golder & Tellis 2004,
  as stated by Stremersch & Tellis 2004).
* **Statistics for few countries.** Two-way fixed effects with the wild-cluster restricted bootstrap (P3);
  Callaway–Sant'Anna difference-in-differences with **exact randomization inference** (P4); Holm corrections; lead and
  placebo checks.

## 4 · Results by research question

### RQ1 · Measuring booms (P2)
| Status | Series |
|---|---|
| Boom | 11 (incl. 6 online-travel 2022 COVID rebounds) |
| Spike | 10 (mostly crypto and fintech firm-formation waves) |
| No datable takeoff | 34 (25 growing, 7 flat, 2 declining through the window) |

Dated booms outside travel: Cambodia mobile money (2011), Indonesia mobile banking (2016) and mobile money (2017),
Malaysia fintech firm formation (2014), Malaysia e-money (2021).

### RQ2 · Correlates (P3)
| Hypothesis | Result |
|---|---|
| H1 infrastructure → growth | Internet-use coefficients negative (an S-curve saturation pattern), none significant |
| H1 infrastructure → takeoff | Mobile subscriptions: odds ratio 2.2 per SD, p = 0.053, not significant |
| H2 account gap → fintech growth | Wrong sign (−0.35), p = 0.21 |
| H5, H8 | Deferred (H5 later done descriptively; H8 lacks pre-2017 attention data) |

### RQ3 · Causal events (P4)
| Hypothesis | Effect | Exact RI p |
|---|---|---|
| H3 payment rails → mobile money | **+0.19 (≈ +21%)**, no pre-trend | 0.60 |
| H3 payment rails → mobile banking | −0.22 | 0.40 |
| H4a digital-bank licences → mobile banking | −0.15 | 0.51 |
| H4b ride-hailing legalisation | not identifiable (treatments predate data) | — |
| H9 crypto regimes → crypto firm formation | −0.08 | 0.68 |
| H5 super-apps (descriptive) | Indonesia fits (GoPay 2016 → takeoffs 2016–17); Cambodia took off first with no anchor | — |

### RQ4–5 · Diffusion (P5)
| Hypothesis | Result |
|---|---|
| H6a China as common an origin as the US | US 3–3.5, China 1, India ~1, SEA-native 1; p = 0.63 (uninformative) |
| H6b China-origin arrives faster | 3 vs 8 years, p = 0.005, but China-origin = crypto exchanges only |
| H7 consistent SEA order / SG or ID first | Kendall's W 0.16–0.24, not significant; SG/ID first no more than chance |

### RQ6 · Out-of-sample validation (P6)
Not answerable: no driver survived P3–P4, and the 2021–2025 window holds two takeoffs. The frozen catalogue and code
allow a genuine re-test in 2028–2030.

## 5 · Limitations

1. **Few countries (6–11) and short series.** All tests can detect only large effects.
2. **Digital takeoffs predate the data.** e-Conomy SEA's online editions start in 2019. Euromonitor's online food series starts in 2020.
3. **Orbis survivorship.** The export holds active firms only and excludes firms without recent financials. Indonesian
   firms are likely undercounted (English keyword search).
4. **Launch ≠ takeoff.** Diffusion was measured by first scaled launch, which involves judgement where smaller players came earlier.
5. **Hand-coded data.** Events, anchors and launches are sourced (two sources where possible), but they are judgement calls.
6. **COVID.** The 2020–22 shock overlaps several events (QRIS mandate) and creates the 2022 travel rebound.

## 6 · What would change the answer

| Upgrade | Why |
|---|---|
| Monthly central-bank series (QRIS, PromptPay, DuitNow, InstaPay) | 12× the data points per country for H3, the most promising lead |
| Orbis re-export including inactive firms | Separates real booms from bubbles in crypto/fintech firm formation |
| Comparison countries (South Asia, Latin America) | More clusters lift statistical power for P3–P4 |
| Deal data (PitchBook / Preqin via UCL) | Capital flows as an outcome and a driver |
| Re-run the frozen pipeline in 2028–2030 | A true out-of-sample test of today's catalogue |

## 7 · Reproducing this work

```
notebooks/00_data_audit         P0  what data exists
notebooks/00b_event_timeline    P1  hand-coded events
notebooks/01_outcome_data       P2  outcome panel
notebooks/02a / 02b             P2  blind coding sheets
notebooks/02_boom_catalogue     P2  takeoff rule, validation, catalogue
notebooks/03_panel_correlates   P3  H1, H2
notebooks/04_causal_events      P4  H3, H4, H9, H5
notebooks/05_diffusion          P5  H6, H7
notebooks/06_validation         P6  RQ6
PREREGISTRATION.md              frozen plan + 29 logged deviations
```

UCL-licensed data (Orbis, Passport) are in `data/licensed/` and are never shared. All other inputs are public and re-fetchable
with `python -m drivers.fetch <source>`.

## References

* Golder, P. N. & Tellis, G. J. (1997). Will it ever fly? Modeling the takeoff of really new consumer durables. *Marketing Science*, 16(3), 256–270.
* Golder, P. N. & Tellis, G. J. (2004). Growing, growing, gone. *Marketing Science*, 23(2).
* Stremersch, S. & Tellis, G. J. (2004). Understanding and managing international growth of new products. *International Journal of Research in Marketing*, 21(4).
* Tellis, G. J., Stremersch, S. & Yin, E. (2003). The international takeoff of new products. *Marketing Science*, 22(2), 188–208.
* Callaway, B. & Sant'Anna, P. H. C. (2021). Difference-in-differences with multiple time periods. *Journal of Econometrics*, 225(2), 200–230.
* Phillips, P. C. B., Shi, S. & Yu, J. (2015). Testing for multiple bubbles. *International Economic Review*, 56(4).
* Google, Temasek & Bain & Company. *e-Conomy SEA* (2021–2025 editions and country reports).
