"""
Shared configuration for the SEA Boom Drivers project.

Every notebook imports from here, so countries, sectors, indicator codes and source
definitions live in exactly one place. See RESEARCH_DESIGN.md for the reasoning.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "public" / "raw"
PROC = ROOT / "data" / "public" / "processed"
LICENSED = ROOT / "data" / "licensed"          # UCL-licensed extracts: never shared
FIG = ROOT / "reports" / "figures"
for p in (RAW, PROC, LICENSED, FIG):
    p.mkdir(parents=True, exist_ok=True)

USER_AGENT = "Mozilla/5.0 (sea-boom-drivers research project)"
START_YEAR, END_YEAR = 2010, 2026

# ---------------------------------------------------------------------------
# Countries: all 11 Southeast Asian states, in two data tiers (design §2.1)
# ---------------------------------------------------------------------------
COUNTRIES = {
    # iso3: (name, iso2, tier)
    "IDN": ("Indonesia", "ID", "A"),
    "MYS": ("Malaysia", "MY", "A"),
    "PHL": ("Philippines", "PH", "A"),
    "SGP": ("Singapore", "SG", "A"),
    "THA": ("Thailand", "TH", "A"),
    "VNM": ("Vietnam", "VN", "A"),
    "BRN": ("Brunei", "BN", "B"),
    "KHM": ("Cambodia", "KH", "B"),
    "LAO": ("Laos", "LA", "B"),
    "MMR": ("Myanmar", "MM", "B"),
    "TLS": ("Timor-Leste", "TL", "B"),
}
TIER_A = [k for k, v in COUNTRIES.items() if v[2] == "A"]
TIER_B = [k for k, v in COUNTRIES.items() if v[2] == "B"]
NAME = {k: v[0] for k, v in COUNTRIES.items()}
# Reference countries for diffusion analysis (RQ4): possible origins of SEA booms
ORIGINS = {"USA": "United States", "CHN": "China", "IND": "India"}

# ---------------------------------------------------------------------------
# Sectors (design §2.2). `outcome` = primary outcome source for the boom catalogue.
# ---------------------------------------------------------------------------
SECTORS = {
    # ---- Fintech: central-bank payment volumes + IMF Financial Access Survey
    "digital_payments":   dict(group="fintech", outcome="central_bank+imf_fas"),
    "qr_realtime_rails":  dict(group="fintech", outcome="central_bank"),
    "digital_lending":    dict(group="fintech", outcome="central_bank+econsea"),
    "digital_banks":      dict(group="fintech", outcome="central_bank"),
    "remittances":        dict(group="fintech", outcome="econsea+worldbank"),
    "retail_investing":   dict(group="fintech", outcome="econsea"),
    "insurtech":          dict(group="fintech", outcome="econsea"),
    # ---- Crypto & blockchain: crypto-specific sources, netted against the global cycle
    "crypto_trading":     dict(group="crypto", outcome="regulators+chainalysis+coingecko"),
    "crypto_ecosystem":   dict(group="crypto", outcome="coingecko+developers+firm_formation"),
    "stablecoins_tokenisation": dict(group="crypto", outcome="regulators+chainalysis"),
    "web3_gaming":        dict(group="crypto", outcome="chainalysis+trends"),
    # ---- Other digital sectors: e-Conomy SEA GMV
    "ecommerce":          dict(group="digital", outcome="econsea"),
    "transport":          dict(group="digital", outcome="econsea"),
    "food_delivery":      dict(group="digital", outcome="econsea"),
    "online_media":       dict(group="digital", outcome="econsea"),
    "online_travel":      dict(group="digital", outcome="econsea"),
}

# ---------------------------------------------------------------------------
# Public indicator codes
# ---------------------------------------------------------------------------
# World Bank WDI / Findex (drivers, design §4)
WB_INDICATORS = {
    "IT.NET.USER.ZS": "internet_users_pct",
    "IT.CEL.SETS.P2": "mobile_subs_per100",
    "FX.OWN.TOTL.ZS": "account_ownership_pct",          # Findex (survey years only)
    "NY.GDP.PCAP.PP.KD": "gdp_pc_ppp",
    "NY.GDP.MKTP.CN": "gdp_lcu",                       # local-currency GDP, for Euromonitor shares
    "SP.URB.TOTL.IN.ZS": "urban_pct",
    "SP.POP.TOTL": "population",
    "SP.POP.1564.TO.ZS": "working_age_pct",
    "SP.POP.0014.TO.ZS": "children_0_14_pct",          # adults (15+) = population x (1 - this)
    "BX.TRF.PWKR.CD.DT": "remittance_inflows_usd",
    "BX.TRF.PWKR.DT.GD.ZS": "remittance_inflows_pct_gdp",
    "EG.ELC.ACCS.ZS": "electricity_access_pct",
    "FS.AST.PRVT.GD.ZS": "private_credit_pct_gdp",
}

# IMF Financial Access Survey (fintech outcomes, harmonised across countries)
IMF_FAS_INDICATORS = {
    "FA65": "mobile_money_tx_value_pct_gdp",
    "FA66N": "mobile_money_tx_per_1000_adults",
    "FA67N": "mobile_money_accounts_per_1000_adults",
    "FA64": "mobile_money_balances_pct_gdp",
    "FA60": "mobile_internet_banking_tx_value_pct_gdp",
    "FA37N": "mobile_internet_banking_tx_per_1000_adults",
}

# e-Conomy SEA reports that are still downloadable (each edition also reports back-years)
ECONSEA_REPORTS = {y: f"https://services.google.com/fh/files/misc/e_conomy_sea_{y}_report.pdf"
                   for y in range(2021, 2026)}

OXCGRT_URL = ("https://raw.githubusercontent.com/OxCGRT/covid-policy-dataset/main/"
              "data/OxCGRT_compact_national_v1.csv")
