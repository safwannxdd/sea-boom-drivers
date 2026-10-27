# What Makes a Sector Boom in Southeast Asia?

**Status:** DRAFT v2 research design. Decisions from review incorporated. No code yet.
**Type:** personal research project. Separate from `~/sea-boom-radar`, and does not depend on it.

---

## 0. Why this project exists

An earlier study (`~/sea-boom-radar`) assumed SEA booms start as San Francisco trends and tested whether SF signals
predict them. That assumption turned out weak:

1. **SF origin was assumed, not tested.** Booms that started in SEA (super-apps, live commerce) or came from China or
   India (QR payments) were invisible to it.
2. **The SF→SEA link is real but weak, and tighter for hype than for booms.** Same-sector links beat placebo pairs
   (p = 0.012), but hype transmitted 11/11 times and booms only 4/7.
3. **Booms were hand-labelled,** which isn't good enough for causal claims.

This project reverses the direction: **start from booms measured inside SEA, then work backwards to the conditions
that preceded and plausibly caused them, wherever the idea came from.**

---

## 1. Research questions

| # | Question | Type |
|---|---|---|
| **RQ1** | How can a sector boom in an SEA country be identified from data, and where is each sector-country in its lifecycle today? | Measurement |
| **RQ2** | Which conditions reliably *come before* booms, at country and regional level? | Correlation |
| **RQ3** | Which of those conditions have a defensible *causal* effect? | Causal inference |
| **RQ4** | Where do SEA booms come from (US, China, India, other SEA countries, home-grown), and with what lag? | Diffusion |
| **RQ5** | Within SEA, do booms spread between countries in a consistent order? | Diffusion |
| **RQ6** | Do the drivers found in RQ2–RQ3 predict booms out of sample? | Validation |

---

## 2. Scope

### 2.1 Countries: all 11 Southeast Asian states

Brunei, Cambodia, Indonesia, Laos, Malaysia, Myanmar, Philippines, Singapore, Thailand, Timor-Leste, Vietnam.

Data coverage is uneven, so countries fall into two tiers. The tiers set which outcome is available, not whether a
country is included.

| Tier | Countries | Outcome data available |
|---|---|---|
| **A** | Indonesia, Malaysia, Philippines, Singapore, Thailand, Vietnam | e-Conomy SEA + central-bank payment statistics + crypto sources |
| **B** | Brunei, Cambodia, Laos, Myanmar, Timor-Leste | central-bank and IMF/World Bank statistics only; no e-Conomy SEA coverage |

Tier B adds what Tier A lacks: countries at earlier stages and with different policy choices. Examples are
Cambodia's Bakong central-bank payment system, Myanmar's post-2021 disruption, and Timor-Leste's late digitalisation.
Expect gaps; Myanmar data after 2021 especially may be unreliable.

### 2.2 Sectors

| Group | Sectors | Main outcome source |
|---|---|---|
| **Fintech** | digital payments & e-wallets, QR / real-time payments, digital lending & BNPL, digital banks, remittances, retail investing / wealth, insurtech | **central-bank payment volumes** (plus IMF Financial Access Survey) |
| **Crypto & blockchain** | exchanges & trading, crypto infrastructure/data firms (e.g. CoinGecko, Kuala Lumpur), stablecoins & tokenisation, Web3 gaming | crypto-specific sources (§3.3) |
| **Other digital sectors** | e-commerce, transport (ride-hailing), food delivery, online media, online travel | **e-Conomy SEA** (Google, Temasek, Bain) |

### 2.3 Period
2010–2026 where data allows. Most outcome series start between 2015 and 2017.

---

## 3. Outcomes: measuring a boom (RQ1)

### 3.1 Outcome sources by sector group (public data first)

| Sector group | Primary outcome | Cross-checks |
|---|---|---|
| Other digital | e-Conomy SEA gross merchandise value (GMV) by vertical × country (annual reports, 2016–2025; manual extraction from PDFs) | Google Trends (local terms), GDELT news volume |
| Fintech | Central-bank payment statistics: BI (QRIS, e-money), BNM (e-money, DuitNow), BOT (PromptPay), BSP (InstaPay/PESONet), MAS, SBV/NAPAS, NBC (Bakong), BOL, CBM, BDCB, BCTL | IMF Financial Access Survey (mobile-money transactions, harmonised), World Bank Findex |
| Crypto | Regulator statistics where published (e.g. Indonesia Bappebti/OJK monthly crypto transaction value and users; Thailand SEC digital-asset trading data; Malaysia SC registered exchanges) | Chainalysis Global Crypto Adoption Index (annual country ranks), CoinGecko API (exchange volumes), Electric Capital developer report (developers by country), Google Trends |

### 3.2 Boom definition: anchored in the takeoff literature

The definition borrows from research on how new products and technologies **take off** across countries. That
literature faces this exact problem: dating when a category moves from niche to mass adoption, comparably across
countries.

| Stage | Definition | Source |
|---|---|---|
| **Takeoff** | First year the outcome's growth exceeds a **threshold that falls as the base gets larger** (large % growth is easy from a tiny base, so the bar is higher there) | Golder & Tellis (1997), *Marketing Science*; applied cross-country by Tellis, Stremersch & Yin (2003), *Marketing Science* |
| **Growth phase** | Years from takeoff until **slowdown** | Golder & Tellis (2004), *Marketing Science*, slowdown definition |
| **Boom** | Takeoff followed by a growth phase of **≥ 3 years** | Our rule. Long enough to exclude one-off spikes, short enough for 2016+ data; sensitivity tested at 2 and 4 years |
| **Spike (not a boom)** | An **explosive episode** that collapses > 50% from peak within 24 months | Explosive-episode test from Phillips, Shi & Yu (2015), *International Economic Review*; 50% rule follows the retention result in the earlier radar study |
| **Maturity / decline** | After slowdown: growth near zero, or a sustained fall | Golder & Tellis (2004) |

The exact threshold curve and slowdown rule will be **transcribed from the papers into `PREREGISTRATION.md` in
phase P1**, before any driver data is looked at.

The result is a **lifecycle stage for every sector × country × year**: pre-takeoff → takeoff → growth → maturity
or decline, or spike. That serves two purposes: dating past booms (needed for RQ2–RQ6) and saying where each market
stands today.

### 3.3 Crypto needs special handling

Crypto activity follows **global price cycles** (2017, 2021, 2024–25). Without care, every SEA country would show
"booms" that are just Bitcoin's price. Two adjustments:

1. **Use local share of global activity as the outcome,** e.g. a country's share of global exchange volume or its
   adoption-index rank, rather than raw volumes. This removes the global cycle.
2. **Separate trading activity from ecosystem building.** Exchange volumes swing with prices. Firm formation,
   developer counts and headcount (e.g. Malaysia's CoinGecko-led cluster) measure whether an industry is actually
   being built locally. Both are tracked, and they may tell different stories.

---

## 4. Candidate drivers (RQ2)

| Family | Example variables | Public source |
|---|---|---|
| **Digital infrastructure** | smartphone penetration, 4G/5G coverage, mobile data price per GB, internet users | ITU, World Bank WDI, cable.co.uk data-price survey |
| **Financial access gaps** | account ownership, card penetration, credit access | World Bank Findex, IMF Financial Access Survey |
| **Payment rails** | launch dates of national QR / real-time payments (PayNow, PromptPay, QRIS, DuitNow, InstaPay/QR Ph, VietQR, Bakong, LAPNet QR) and cross-border QR links | central banks (hand-coded dates) |
| **Regulation** | ride-hailing legalisation, digital-bank licences, lending rules, crypto exchange licensing and bans, regulatory sandboxes | regulators (hand-coded event timeline) |
| **Demography & demand** | median age, urbanisation, GDP per capita (PPP), remittance inflows | World Bank, UN |
| **Capital** | venture and private investment flows by country and sector, big-tech strategic investment | public proxies only at first (press counts, e-Conomy funding totals); see §8 for licensed upgrades |
| **Anchor platforms** | presence of a super-app or marketplace already distributing the category | hand-coded |
| **External diffusion** | same-sector attention in US, China, India before the SEA boom | Google Trends, GDELT |
| **Global crypto cycle** (crypto only) | BTC price, global exchange volume | CoinGecko API |
| **Talent** | tech/developer population | Electric Capital report, GitHub country stats |
| **Shocks** | COVID restrictions | Oxford COVID-19 Government Response Tracker |

---

## 5. Hypotheses (to be frozen in P1)

| # | Hypothesis | Main test |
|---|---|---|
| **H1** | Booms follow **infrastructure thresholds** (smartphone penetration, data price) more than foreign attention | panel with threshold terms |
| **H2** | **Financial-access gaps** speed up fintech booms (leapfrogging: low card use leads to faster e-wallet adoption) | panel with interactions |
| **H3** | Launching a **national QR / real-time payment rail** causes a jump in digital payment volume | staggered difference-in-differences across countries |
| **H4** | **Licensing events** cause sector growth, and **bans** cause collapse | event studies, synthetic control |
| **H5** | Categories distributed through an **existing anchor platform** take off faster | panel with anchor indicator |
| **H6** | SEA booms come from **China as often as from the US**, and China-origin models transfer with a shorter lag | diffusion analysis |
| **H7** | Booms appear first in **Singapore or Indonesia**, then spread in a consistent order | intra-SEA lead-lag |
| **H8** | **Attention without enablers** (high search/news, weak infrastructure or rails) produces spikes, not booms | panel interaction |
| **H9** (crypto) | Local **crypto ecosystem building** (firms, developers) is driven by **regulatory clarity** (licensing regimes), not by local trading volume | event studies on licensing dates; compare Malaysia, Singapore, Thailand, Indonesia, Vietnam |

---

## 6. Methods

### 6.1 Descriptive (RQ1, RQ4)
- **SEA Boom Catalogue:** every sector-country boom and spike since 2010, dated, with lifecycle stage and origin
  attribution. Failures are catalogued too.
- Timelines per sector across countries: who led, who followed, who never took off.

### 6.2 Correlation (RQ2)
- Two-way fixed-effects panel: outcome growth on **lagged** drivers, with sector-country and year fixed effects.
  Standard errors clustered by country. With few clusters, use the wild-cluster bootstrap.
- **Lead tests:** future drivers must not "predict" past outcomes. If they do, it's reverse causality or a shared trend.
- **Placebo drivers** measure the background correlation level, using the same logic as the radar's placebo test.

### 6.3 Causal identification (RQ3)
- **Staggered difference-in-differences** with estimators built for staggered timing (Callaway & Sant'Anna 2021;
  Sun & Abraham 2021), not naive two-way fixed effects. Applied to events that hit countries at different times:
  QR rails, digital-bank licences, ride-hailing legalisation, crypto licensing.
- **Event-study plots** with pre-trend checks. Without flat pre-trends, no causal claim is made.
- **Synthetic control** for single-country shocks (e.g. a crypto ban or one country's payment mandate).
- **Robustness:** alternative outcomes, excluding Singapore (income outlier), excluding COVID years, Tier A only.

### 6.4 Diffusion (RQ4, RQ5)
- Source attribution: lead-lag tests with placebo pairs for US → SEA, China → SEA and India → SEA in the same sector.
- Intra-SEA diffusion network: pairwise country lead-lag per sector, summarised as a "who leads" ranking.

### 6.5 Predictive validation (RQ6)
- Using only drivers established in 6.2–6.3, train on booms resolved by 2020 and test on 2021–2026.
- Benchmarks: a naive "follow the attention" model, and the SF-signal model from the earlier radar study.

---

## 7. Threats to validity

| Threat | Planned answer |
|---|---|
| Few countries means few clusters and weak standard errors | wild-cluster bootstrap, randomisation inference; report effect sizes, not just p-values |
| Reverse causality (booms trigger regulation) | lead tests; event studies with pre-trends; prefer events set by policy timetables |
| Shared regional trends (smartphones, COVID) | year fixed effects; placebo sectors |
| Crypto outcomes driven by global prices | use local share of global activity; global-cycle controls (§3.3) |
| Uneven data across the 11 countries | tiered analysis; every result reported for Tier A and for all countries |
| Hindsight in the boom definition | takeoff rules taken from the literature and frozen in P1 before driver analysis |
| Survivorship (only famous booms recorded) | the catalogue is generated from outcome data, so failures appear automatically |
| Hand-coded event dates | two independent sources per date; event table published with citations |

---

## 8. Data access: public first, then UCL-licensed upgrades

Everything in §3–§4 is public and is the default. These UCL Library databases would strengthen specific weak
spots. Availability was checked against UCL's
[Business and Finance data guide](https://library-guides.ucl.ac.uk/data-statistics/business-finance).

| Database (UCL) | What it adds to this project | Fills which gap |
|---|---|---|
| **PitchBook** | Deal-level venture and private investment by country, sector and stage; company founding dates | capital driver; firm formation as an outcome; the single biggest upgrade |
| **Preqin Pro** (also Preqin deal datasets inside **WRDS**) | Fund flows and deals into SEA, investor activity | capital driver; cross-check against PitchBook |
| **Orbis** (+ Orbis M&A) | Firms by incorporation date and industry code in every country; M&A transactions | firm formation (e.g. count Malaysian crypto/blockchain firms by year); exits |
| **EMIS** | Emerging-markets company, industry and local-news coverage | Tier B countries, where public data is thinnest |
| **Euromonitor Passport** | Market sizes by country and category (digital payments, e-commerce) | independent outcome cross-check against e-Conomy SEA |
| **LSEG Workspace** | Deals, listed-company data | exits and listings; licences are issued for 1 week at a time, so plan bulk downloads |
| **Nexis**, **Bloomberg.com** | News archives | dating regulatory events; news-volume measures |
| **Statista** | Aggregated secondary statistics | quick cross-checks only; always trace to the original source |
| **S&P Capital IQ Pro**, **CEIC** | Transactions and private-company data; harmonised Asian macro and payment series | ⚠ found via search but not on the guide page; confirm with UCL Library. CEIC could save weeks of central-bank data cleaning |

**Licence caution:** university database licences are usually limited to non-commercial academic and educational
use, and restrict sharing raw data. Check each database's terms before using it in a personal project, and keep
licensed data in a separate folder outside anything shared publicly. If this work is ever used commercially, the
licensed data and anything derived from it cannot come along. Published results must then rest on the public data.

---

## 9. Planned repository structure

```
sea-boom-drivers/
├── RESEARCH_DESIGN.md              ← this file
├── PREREGISTRATION.md              ← boom definition + hypotheses, frozen in P1
├── drivers/
│   ├── config.py                   ← countries, tiers, sectors, terms, thresholds
│   ├── fetch.py                    ← cached public-data fetchers
│   └── events.csv                  ← hand-coded regulatory / payment-rail / crypto-licensing timeline, with sources
├── notebooks/
│   ├── 00_data_audit.ipynb               ← P0: what exists, coverage, effort
│   ├── 01_outcome_data.ipynb             ← collect outcome series by sector group
│   ├── 02_boom_catalogue.ipynb           ← RQ1: takeoff / growth / slowdown / spike dating; lifecycle stages
│   ├── 03_driver_data.ipynb              ← collect and align drivers
│   ├── 04_panel_correlates.ipynb         ← RQ2
│   ├── 05_causal_events.ipynb            ← RQ3
│   ├── 06_diffusion_sources.ipynb        ← RQ4–5
│   └── 07_predictive_validation.ipynb    ← RQ6
├── data/
│   ├── public/                     ← shareable
│   └── licensed/                   ← UCL-licensed extracts; never shared or committed
└── reports/
```

Same conventions as the radar: notebook-style code with clearly separated sections, `.py` sources in
`notebooks/_src/`, cached fetchers, and no look-ahead in any predictive step.

---

## 10. Phases

| Phase | Output | Go / no-go check |
|---|---|---|
| **P0 · Data audit** | per-source table: availability, coverage, format, effort; e-Conomy SEA figures extracted | at least one outcome covering ≥ 6 countries × ≥ 8 years per sector group; otherwise narrow that group |
| **P1 · Pre-registration** | takeoff and slowdown rules transcribed from the literature, hypotheses, event table | you sign off |
| **P2 · Boom catalogue** | dated booms, spikes and lifecycle stages | sanity-check against known history (GoPay, QRIS, Grab, Axie, Indonesian crypto) |
| **P3 · Correlates** | H1, H2, H5, H8 | — |
| **P4 · Causal** | H3, H4, H9 | pre-trends pass |
| **P5 · Diffusion** | H6, H7 | — |
| **P6 · Validation + write-up** | out-of-sample test; final report | — |

---

## 11. Decisions log

| # | Decision | Status |
|---|---|---|
| 1 | Scope: digital sectors, with fintech and crypto/blockchain as focus groups | ✅ decided |
| 2 | Outcomes: e-Conomy SEA for digital sectors; central-bank payment volumes for fintech; crypto-specific sources for crypto | ✅ decided |
| 3 | Boom thresholds: taken from the takeoff literature (§3.2), frozen in P1 | ✅ decided |
| 4 | Data: public first; UCL databases as upgrades after licence-terms check (§8) | ✅ decided |
| 5 | Countries: all 11 SEA states, in two data tiers | ✅ decided |
| 6 | Separate study from `sea-boom-radar` | ✅ decided |
| 7 | Personal research project | ✅ decided |
| 8 | Outputs designed to be read at sector × country level: lifecycle stage, takeoff timing, durability, market size | ✅ decided |

---

## References (to be verified in P1)

- Golder, P. N. & Tellis, G. J. (1997). Will it ever fly? Modeling the takeoff of really new consumer durables. *Marketing Science*, 16(3).
- Tellis, G. J., Stremersch, S. & Yin, E. (2003). The international takeoff of new products: The role of economics, culture, and country innovativeness. *Marketing Science*, 22(2).
- Golder, P. N. & Tellis, G. J. (2004). Growing, growing, gone: Cascades, diffusion, and turning points in the product life cycle. *Marketing Science*, 23(2).
- Phillips, P. C. B., Shi, S. & Yu, J. (2015). Testing for multiple bubbles. *International Economic Review*, 56(4).
- Callaway, B. & Sant'Anna, P. H. C. (2021). Difference-in-differences with multiple time periods. *Journal of Econometrics*, 225(2).
- Sun, L. & Abraham, S. (2021). Estimating dynamic treatment effects in event studies with heterogeneous treatment effects. *Journal of Econometrics*, 225(2).
- Google, Temasek & Bain & Company. *e-Conomy SEA* reports (annual, 2016–2025).
