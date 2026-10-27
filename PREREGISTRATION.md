# Pre-registration: SEA Boom Drivers

**Status:** 🔒 **FROZEN on 2026-10-07** (approved after P1 review). Any change from here on is recorded in the
Deviations Log (§9) with a date and a reason, and the original text stays.

**Closed on 2026-10-11:** all phases (P0–P6) were executed under this plan. **29 deviations** are logged in §9. Results
per hypothesis are in `reports/FINAL_REPORT.md` §4:

| Hypothesis | Outcome |
|---|---|
| H1 infrastructure | Not supported (mobile-subscription takeoff hazard borderline, p = 0.053) |
| H2 financial-access gap | Not supported (wrong sign) |
| H3 payment rails | Not supported (+21% mobile money, p = 0.60) |
| H4 licences / bans | H4a not supported; H4b not identifiable; H4c not testable |
| H5 anchor platforms | Descriptive only; mixed |
| H6 origins | H6a uninformative; H6b significant but rests on one category |
| H7 intra-SEA order | Not supported |
| H8 attention × enablers | Not testable (no pre-2017 attention data) |
| H9 crypto regulation | Not supported |
| RQ6 out-of-sample | Not answerable (no surviving drivers; 2 test takeoffs) |

**Why this exists:** the earlier SF radar study had to retract a result because its evaluation windows were set
after looking at data. Writing every definition and test down *before* collecting outcomes stops that from
happening again.

**Rule of order:** the boom catalogue (P2) is built and frozen before any driver data is compared with outcomes
(P3 onward).

---

## 1. Outcome series (what "activity" means per sector group)

| Group | Primary outcome | Normalisation (the "penetration" analogue) | Years | Countries |
|---|---|---|---|---|
| **Fintech** | IMF FAS value of **mobile-money** transactions, and separately of **mobile & internet banking** transactions | already % of GDP | 2007–2025 (varies) | 6 pass the 8-year rule (ID, MY, PH, TH, VN, KH); SG via MAS data |
| Fintech (secondary) | Central-bank rail volumes: QRIS, DuitNow, PromptPay, InstaPay/PESONet, PayNow, Bakong | transactions per adult | from each rail's launch | Tier A + Cambodia |
| **Digital sectors** | e-Conomy SEA **GMV by country × sector** (e-commerce, transport, food delivery, online travel, online media) | GMV as % of GDP | **2019–2025** (7 years; approved deviation from the 8-year rule) | Tier A |
| **Crypto** | (a) country **share of global** activity (Chainalysis index rank; regulator trading value ÷ global exchange volume), and (b) **firm formation**: new crypto/blockchain firms per year (Orbis) | (a) is a share already; (b) firms per million population | ~2019–2025 for (a); ~2010–2025 for (b) | where available |

Only **actual** figures are used. Forecast years (e.g. "2025F" in older e-Conomy editions, and 2030) are excluded.
When editions disagree about the same year, the **most recent edition** wins, because later editions revise earlier estimates.

---

## 2. Lifecycle stages

Every sector × country × year is assigned one stage:
**pre-takeoff → takeoff → growth → slowdown → maturity / decline**, plus **spike** for explosive episodes that reverse.

### 2.1 Takeoff: threshold rule (Golder & Tellis 1997; Tellis, Stremersch & Yin 2003)

**What the literature actually says (verified against the papers):**
- Golder & Tellis (1997) define takeoff as *"the first year a product's relative growth crosses the threshold"*.
  The threshold is a curve of **percentage sales growth against base sales**: high growth is required from a
  small base, less from a large one. They add a **minimum base** (50,000 units), because *"large percentage
  increases from a smaller base level of sales were not a reliable indicator of takeoff"*.
- The threshold was drawn as a figure for US consumer durables in unit sales. **No formula was published.**
- Tellis, Stremersch & Yin (2003) adapted it across 16 countries using **penetration** as the base. They
  specified the threshold *"heuristically… iterat[ing] between identifying takeoff years, based on a threshold
  function, and visual identification"*, keeping the curve that best matched visual identification
  (as described by Van Everdingen, Fok & Stremersch 2009).

There is no formula to copy, so this project **replicates their calibration procedure**:

| Step | Rule (frozen) |
|---|---|
| **Threshold family** | required growth `g*(L) = a · L^(−b)`, where `L` = normalised level (§1) in the base year, `a > 0`, `b ≥ 0`. A decreasing curve, as in both papers. |
| **Minimum base** | no takeoff while `L < L_min` (analogue of the 50,000-unit floor) |
| **Takeoff year** | first year `t` with `growth(t-1→t) ≥ g*(L_{t-1})` and `L_{t-1} ≥ L_min`. A takeoff happens at most once per series. |
| **Calibration set** | a random half of all outcome series (seed fixed in code), stratified by sector group |
| **Visual coding** | you mark the takeoff year on **anonymised charts** (no country or sector name, axes rescaled) **before** the parameters are fitted. "No takeoff" is an allowed answer. |
| **Fitting** | grid search over `a`, `b`, `L_min` to maximise exact-year agreement with the visual codes (ties broken by ±1-year agreement, then the simplest curve) |
| **Validation** | apply the fitted rule to the **other half**. Golder & Tellis report > 90% agreement; we require **≥ 75% exact or ±1-year agreement**, otherwise the rule is revised once and the revision is logged in §9. |
| **Robustness** | both alternatives from Golder & Tellis (1997, Appendix): **logistic-curve rule** (maximum of the second derivative of a fitted logistic) and **maximum-growth rule** (largest % increase within 3 years of the logistic takeoff). Results are reported under all three. |

The calibration is done **separately per sector group**, because fintech (% of GDP), digital (GMV % of GDP) and
crypto (shares) live on different scales.

### 2.2 Slowdown, boom, spike, maturity

| Stage | Rule | Source |
|---|---|---|
| **Slowdown** | first year after takeoff in which the outcome is **≥ 15% below its previous peak** and **stays below that peak for all remaining observed years (minimum 2)** | Golder & Tellis (2004) define slowdown as a 15% decline that stays below the previous peak for 5 years. ⚠ To be checked against the full text (via UCL). Our panels are too short for 5 years, so that part is shortened; this is a known deviation. |
| **Growth phase** | takeoff year up to the year before slowdown (or to the last observed year) | Golder & Tellis (2004) |
| **Boom** | takeoff followed by **≥ 3 years** without slowdown | our rule (design §3.2). Sensitivity at 2 and 4 years. |
| **Boom pending** | takeoff with fewer than 3 years observed since | right-censored, kept as its own category, never counted as boom or non-boom |
| **Spike** | (a) **monthly/quarterly series** (rails, crypto): an explosive episode by the Phillips, Shi & Yu (2015) GSADF test (95% bootstrap critical values) whose level then falls **> 50% from its peak within 24 months**. (b) **annual series:** growth above `g*` followed by a fall **> 50% from peak within 2 years**. | PSY (2015); the 50% rule follows the retention result in the SF radar study |
| **Maturity** | after slowdown, absolute growth < 10% a year | our rule |
| **Decline** | after slowdown, three consecutive years of negative growth | our rule |

---

## 3. Boom catalogue (P2 output)

One row per sector × country, including: takeoff year (all three rules), stage each year, boom / boom pending /
spike / no takeoff, time from first data to takeoff, peak growth, and **origin attribution**:

| Origin | Rule |
|---|---|
| SEA-native | the earliest takeoff of this sector anywhere is in an SEA country |
| US / China / India | the same sector took off first in that country, ≥ 1 year earlier (dated by the same threshold rule on IMF FAS or Google Trends data for the origin country) |
| Intra-SEA | another SEA country took off ≥ 1 year earlier |
| Unattributed | none of the above can be dated |

Attribution is descriptive. RQ4 tests it formally.

---

## 4. Drivers (frozen list)

Drivers come from RESEARCH_DESIGN.md §4. Every driver enters models **lagged by one year**, and no driver may be
added after outcomes are linked to drivers without a §9 log entry. Hand-coded events are in
`drivers/events.csv` (§6).

---

## 5. Hypotheses and exact tests

Significance level **α = 0.05, two-sided**. Within each hypothesis family, p-values are adjusted with **Holm**.
Standard errors are clustered by country with the **wild-cluster bootstrap** (Webb weights, 9,999 draws),
because there are few clusters. Effect sizes are reported with confidence intervals whatever the p-value.

| # | Hypothesis | Outcome | Test | Supported if |
|---|---|---|---|---|
| **H1** | Takeoff follows infrastructure thresholds more than foreign attention | takeoff hazard | discrete-time hazard model: smartphone/internet penetration, data price, origin-country attention (all lagged) | infrastructure terms significant **and** larger in standardised size than origin attention |
| **H2** | Financial-access gaps accelerate fintech takeoff | fintech takeoff hazard; growth-phase slope | hazard model and panel FE with (1 − account ownership) and card penetration | gap coefficient > 0, significant |
| **H3** | National QR / real-time rails cause digital-payment growth | FAS value % GDP; rail volumes | Callaway–Sant'Anna staggered DiD on rail launch dates (E01–E15); not-yet-treated controls | post-launch ATT > 0, significant, **and** pre-trend test not rejected (p > 0.10) |
| **H4** | Licensing events cause growth; bans cause collapse | sector outcome | event studies (same estimator) for digital-bank licences, ride-hailing legalisation, crypto regimes; synthetic control for single-country bans | sign matches `direction` in events.csv, significant, pre-trends pass |
| **H5** | Categories on an anchor platform take off faster | time to takeoff | hazard model with anchor-platform indicator | anchor coefficient > 0, significant |
| **H6** | SEA booms come from China as often as from the US; China-origin transfers faster | origin shares; lag | two-sided binomial test on origin shares; Mann–Whitney on lags | not rejecting equal shares (H6a); China lag shorter, significant (H6b) |
| **H7** | Booms appear first in Singapore or Indonesia, then spread in a consistent order | takeoff-year ranks | Kendall's W across sectors; share of sectors where SG or ID ranks first versus chance | W significant **and** SG/ID first more often than chance |
| **H8** | Attention without enablers produces spikes, not booms | spike vs boom | logistic model: attention (GDELT/Trends) × enabler index | interaction negative for boom and positive for spike, significant |
| **H9** | Crypto ecosystem-building follows regulatory clarity, not trading volume | crypto firm formation | event study on licensing-regime dates (E30–E39), controlling for the trading-volume share | post-regime effect > 0, significant; trading-volume share not significant |

**Not-supported results are reported with the same prominence as supported ones.**

---

## 6. Event table rules (`drivers/events.csv`)

- Every event needs **two independent sources** before analysis (`status = verified`). Events still marked
  `needs_source`, `needs_second_source` or `conflicting_sources` are resolved in P2 data collection. Any that
  cannot be resolved are **dropped**, not guessed.
- The event date is when the rule **took effect**, not when it was announced. If only an announcement date
  exists, that is recorded and flagged.
- `direction`: `+` enabling, `−` restricting, `0` administrative (e.g. a change of regulator).

---

## 7. Out-of-sample validation (RQ6)

- **Training:** sector-country booms whose status is resolved by **end-2020**.
- **Test:** takeoffs and booms from **2021–2025**.
- **Model:** only drivers that survived P3–P4. Benchmarks: (i) a "follow the attention" model, and (ii) the SF-signal
  score from the earlier radar study.
- **Metric:** AUC with sector-cluster bootstrap CI, and the Brier score.

---

## 8. Data requests for P2

1. **TinyFish downloads:** BNM and BSP payment-statistics files (both sites block scripts), into
   `data/public/raw/central_banks/`.
2. **e-Conomy SEA transcription:** 30 country reports (2021–2025 × 6 countries). Each number is double-checked
   against the chart image and logged with page reference.
3. **Orbis export (you, via UCL):** see the specification below. Saved to `data/licensed/orbis/`.

**Orbis export specification**

| Setting | Value |
|---|---|
| Countries | all 11 SEA countries |
| Firms | active **and** inactive (inactive firms are needed to avoid survivorship bias) |
| Search | trade description / products contains any of: *cryptocurrency, crypto, blockchain, digital asset, digital token, virtual asset, Web3, DeFi, NFT, stablecoin, bitcoin*. Run a **second export** for fintech: *e-wallet, digital payment, payment gateway, peer-to-peer lending, buy now pay later, digital bank, remittance, robo-advis*. |
| Fields | BvD ID, company name, country, city, **date of incorporation**, status and status date, NACE Rev. 2 core code, US SIC, trade description (English), number of employees (latest + history if available), operating revenue (latest), shareholders' country |
| Format | Excel or CSV, one file per search |

---

## 9. Deviations log

| Date | Section | Change | Reason |
|---|---|---|---|
| 2026-10-07 | §1 | Digital sectors use 7 years (2019–2025) instead of the 8-year minimum | P0 audit: no longer series exists publicly; approved by you; Euromonitor Passport held in reserve |
| 2026-10-07 | §2.1 | Threshold rule replicated by procedure, not by formula | Neither source paper publishes a formula (verified in text) |
| 2026-10-07 | — | Frozen. Approved: visual takeoff coding by the author, 75% validation bar, 10% maturity cut-off | P1 review |
| 2026-10-07 | §2.2 | Slowdown "stays below peak" shortened from 5 years to all remaining observed years (min. 2) | Panels too short; G&T 2004 definition still to be verified in full text |
| 2026-10-08 | §2.2 | **Slowdown rule replaced** (supersedes the row above): the growth phase ends in *"the first year, after takeoff, after which two consecutive years occur with lower sales"* (the G&T 2004 rule as stated by Stremersch & Tellis 2004, *IJRM* 21(4), verified in text). Slowdown = the year after that end-of-growth year. | The "15% / 5 years" wording came from a secondary summary and could not be found in the paper; the primary-source rule needs only 2 years after the peak |
| 2026-10-08 | §1 | Digital sectors: the primary analysis uses **6 actual years (2019–2024)**; the 2025 H1-annualised estimate is a sensitivity run only. Series are **chain-linked** with the newest edition's growth rates. | "Actual figures only" rule; editions revise earlier years (e.g. Indonesia 2019 travel 10.1 → 7) |
| 2026-10-08 | §2.1 | Coding categories: "Y1" codes are treated as "before data" (no growth is observable into Y1); the rule's first detectable crossing (Y2) maps to the same "start" category. Added a "before" option to the sheet. | Most e-Conomy series were already growing in 2019 |
| 2026-10-08 | §2.1 | The threshold is calibrated on **% of GDP series only** (IMF FAS, e-Conomy). The 2 rail series (transactions per adult, Malaysia) use the visual code only. | Two series cannot calibrate a unit-specific curve |
| 2026-10-08 | §2.2 | PSY explosive-episode test deferred: no monthly series are in the catalogue yet; the annual spike rule (b) is used | Philippines InstaPay extraction failed; crypto monthly data not yet collected |
| 2026-10-08 | §2.1 | **Revision A (the one permitted revision):** after the first validation failed (±1-year agreement 50% digital, 60% fintech vs the 75% bar), the categories "already growing at start" and "no takeoff" are merged into **"no datable takeoff in the window"**, and the rule is refit on the calibration half. Agreement is reported under both definitions. Catalogue status for these series: "no datable takeoff (growing/flat/declining through window)"; they are not counted as booms. | 8 of the 13 misses were exactly this overlap; both answers mean no takeoff is datable inside a 6-year window. Decided by the author in the P2 review. |
| 2026-10-08 | §2.2 | COVID-rebound rule considered and **rejected** in the P2 review; the 2022 online-travel takeoffs stand, with a caveat | Author's decision |
| 2026-10-08 | §1 | **Orbis company exports used as received**, despite filters for active firms only and excluding firms without recent financial data. Firm-formation results carry a survivorship-bias caveat; Indonesian firms likely undercounted (English keyword search). Firm-formation series are dated by **visual code only** (unit: firms, not % of GDP). | Author's decision in the P2 review |
| 2026-10-08 | §1 | **Euromonitor Passport "Consumer Foodservice Online Ordering" (2020–2025)** added as a food-delivery-only series and a cross-check on e-Conomy SEA, scaled by World Bank local-currency GDP. It is dated with the **frozen** digital threshold (no refitting), and agreement with blind visual codes is reported as an out-of-sample test. | Passport does not track online ordering before 2020 |
| 2026-10-08 | §2.1 | **Sheet 2 recoded after an instruction clarification** (before any sheet-2 key or result was seen): a multi-year rise that later crashes is coded at the year the rise began (crash handled by the spike/slowdown rules); one-year blips are "none". First attempt (17/18 "none") kept as `visual_codes_2_first_attempt.csv`. | The coder asked how to code rise-then-crash charts; the original wording ("dramatic, sustained") was ambiguous for volatile count data |
| 2026-10-09 | §5 H1 | Foreign/origin-attention comparison **not run**: Google Trends/GDELT attention exists only from 2017, after most takeoffs. H1 tested on infrastructure terms only; the origin comparison moves to P5 (diffusion). The online-travel 2022 rebounds are excluded from the hazard (not takeoffs from zero). | Data availability |
| 2026-10-09 | §5 H2 | Card penetration dropped (no public panel). Findex account ownership linearly interpolated between survey years and held flat after the last survey | Data availability |
| 2026-10-09 | §5 | Firm-formation outcome in the panel models = asinh(new firms per million), a formation rate (the flow is already the growth of the firm stock); 2025 excluded (Orbis registration lag) | Outcome is a flow, not a level |
| 2026-10-09 | §5 H5, H8 | **Deferred**: H5 needs a sourced anchor-platform table (to be coded with the P4 events); H8 needs attention data before 2017 | Data availability |
| 2026-10-11 | §5 H3/H4/H9 | **Treatment timing rule:** an event taking effect Jan–Jun treats that year; Jul–Dec treats the next year (annual data). A cohort counts only if its onset falls inside the unit's own observed years; otherwise the unit is never-treated in the window | Annual outcomes; rule fixed before estimation |
| 2026-10-11 | §5 H3/H4/H9 | Inference by **exact randomization inference** over reassignments of onset years (instead of the wild-cluster bootstrap) | 4–8 units per test; RI is exact at any N (listed among the planned answers in design §7) |
| 2026-10-11 | §5 H4 | H4b (ride-hailing) **not identifiable**: Philippines and Indonesia were treated before e-Conomy data starts. H4c (bans) **not testable**: no outcome series. Synthetic control not run (no single-country shock with an outcome series) | Data availability |
| 2026-10-11 | §5 H9 | The trading-volume-share control was **not possible** (Chainalysis ranks only from 2022, method changes yearly) | Data availability |
| 2026-10-11 | §5 H5 | Anchor-platform table coded (`drivers/anchors.csv`, two sources each); H5 reported **descriptively** (3–4 dated fintech takeoffs) instead of with a hazard model | Too few events |
| 2026-10-11 | §6 | Event E03 (PromptPay, Jan 2017) verified with a second source (Oxford Business Group, Bangkok Post) | Needed for H3 |
| 2026-10-11 | §3, §5 H6/H7 | **Diffusion measured by launch dates, not takeoff dates**: hand-built `drivers/launches.csv` (6 categories × 6 SEA + US/China/India; first scaled app-based player). Takeoffs cannot be dated for most digital sectors (pre-2019) or for origin countries. All tests run on all dates and on two-source dates only | Data availability |
| 2026-10-11 | §5 H3 | Monthly rerun of H3 **not done**: only Thailand has monthly data covering the pre-launch period (Indonesia's QRIS mandate coincides with COVID; Malaysia's series starts after DuitNow); a one-country design is weaker than the frozen DiD. Recorded as future work | Feasibility check; author's decision |
| 2026-10-11 | §5 H1 | The origin-attention comparison deferred from P3 remains **not run**: no pre-2017 attention data | Data availability |
| 2026-10-11 | §7 | RQ6 run as specified: no driver survived P3–P4, so the drivers model is the base rate; the attention benchmark is not runnable (no data) and the SF-radar benchmark is not comparable (sector-level scores). One exploratory check (mobile subscriptions) is reported and labelled as not pre-registered | Outcome of P3–P4 |
| 2026-10-08 | §8 | The Orbis export received is **Orbis M&A** (deals), not the company register. It is kept for the capital driver; crypto firm formation (H9) still needs an Orbis company export | Export inspection |

---

## References

- Golder, P. N. & Tellis, G. J. (1997). Will it ever fly? Modeling the takeoff of really new consumer durables. *Marketing Science*, 16(3), 256–270.
- Tellis, G. J., Stremersch, S. & Yin, E. (2003). The international takeoff of new products. *Marketing Science*, 22(2), 188–208.
- Golder, P. N. & Tellis, G. J. (2004). Growing, growing, gone: Cascades, diffusion, and turning points in the product life cycle. *Marketing Science*, 23(2).
- Stremersch, S. & Tellis, G. J. (2004). Understanding and managing international growth of new products. *International Journal of Research in Marketing*, 21(4). (Source of the verified slowdown rule.)
- Van Everdingen, Y., Fok, D. & Stremersch, S. (2009). Modeling global spill-over of new product takeoff. Erasmus Research Institute working paper ERS-2008-067-MKT (published later in *Journal of Marketing Research*).
- Phillips, P. C. B., Shi, S. & Yu, J. (2015). Testing for multiple bubbles. *International Economic Review*, 56(4), 1043–1078.
- Callaway, B. & Sant'Anna, P. H. C. (2021). Difference-in-differences with multiple time periods. *Journal of Econometrics*, 225(2), 200–230.
