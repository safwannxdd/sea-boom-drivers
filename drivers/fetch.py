"""
Data plumbing: cached fetchers for the public sources.

Each fetcher writes under data/public/raw/<source>/ and reuses the file if it exists,
so re-running a notebook never re-downloads. Delete a file to force a refresh.

Run one source from the shell:
    python -m drivers.fetch worldbank
"""
import io
import json
import sys
import time

import pandas as pd
import requests

from .config import (COUNTRIES, ECONSEA_REPORTS, IMF_FAS_INDICATORS, ORIGINS, OXCGRT_URL,
                     RAW, USER_AGENT, WB_INDICATORS)

S = requests.Session()
S.headers["User-Agent"] = USER_AGENT


def _path(source, name):
    d = RAW / source
    d.mkdir(parents=True, exist_ok=True)
    return d / name


def _get(url, params=None, tries=5, timeout=120, **kw):
    for i in range(tries):
        try:
            r = S.get(url, params=params, timeout=timeout, **kw)
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(10 * 2 ** i)
                continue
            return r
        except requests.RequestException:
            time.sleep(5 * 2 ** i)
    raise RuntimeError(f"failed after {tries} tries: {url}")


# ------------------------------------------------------------------ World Bank
def fetch_worldbank():
    """WDI + Findex indicators for the 11 SEA countries and the 3 origin countries, 2000 onward."""
    f = _path("worldbank", "indicators.parquet")
    if f.exists():
        return pd.read_parquet(f)
    codes = ";".join(list(COUNTRIES) + list(ORIGINS))
    rows = []
    for code, name in WB_INDICATORS.items():
        r = _get(f"https://api.worldbank.org/v2/country/{codes}/indicator/{code}",
                 params={"format": "json", "date": "2000:2025", "per_page": 2000})
        for row in (r.json()[1] or []):
            if row["value"] is not None:
                rows.append(dict(iso3=row["countryiso3code"], year=int(row["date"]),
                                 indicator=name, value=float(row["value"])))
    df = pd.DataFrame(rows)
    df.to_parquet(f)
    return df


# ------------------------------------------------------------------ IMF Financial Access Survey
def fetch_imf_fas():
    """Harmonised fintech outcomes (mobile money, mobile/internet banking) from the IMF FAS."""
    f = _path("imf_fas", "fas.parquet")
    if f.exists():
        return pd.read_parquet(f)
    key = "+".join(list(COUNTRIES) + list(ORIGINS)) + ".*.*.*"
    r = _get(f"https://api.imf.org/external/sdmx/2.1/data/IMF.STA,FAS,5.0.0/{key}",
             params={"startPeriod": 2004},
             headers={"Accept": "application/vnd.sdmx.data+csv;version=1.0.0"}, timeout=300)
    r.raise_for_status()
    d = pd.read_csv(io.StringIO(r.text), low_memory=False)
    d = d[d.INDICATOR.isin(IMF_FAS_INDICATORS)]
    # some codes are published twice (domestic currency AND % of GDP / per adult); keep the scaled version only
    d = d[~d.SERIES_NAME.str.contains("Domestic currency", na=False)]
    assert not d.duplicated(["COUNTRY", "INDICATOR", "TIME_PERIOD"]).any(), "duplicate FAS rows after filtering"
    df = pd.DataFrame(dict(iso3=d.COUNTRY, year=d.TIME_PERIOD.astype(int),
                           indicator=d.INDICATOR.map(IMF_FAS_INDICATORS), value=d.OBS_VALUE.astype(float),
                           series_name=d.SERIES_NAME))
    df.to_parquet(f)
    return df


# ------------------------------------------------------------------ IMF World Economic Outlook
def fetch_imf_weo_gdp():
    """Nominal GDP in current US$ billions (IMF WEO, NGDPD), including the current-year estimate.
    Used to express GMV and payment values as % of GDP."""
    f = _path("imf_weo", "ngdpd.parquet")
    if f.exists():
        return pd.read_parquet(f)
    # this endpoint rejects custom user-agents and ignores country filters, so fetch all and filter
    r = requests.get("https://www.imf.org/external/datamapper/api/v1/NGDPD", timeout=120)
    vals = r.json()["values"]["NGDPD"]
    keep = set(COUNTRIES) | set(ORIGINS)
    df = pd.DataFrame([dict(iso3=c, year=int(y), gdp_usd_b=float(v))
                       for c, ys in vals.items() if c in keep for y, v in ys.items()])
    df.to_parquet(f)
    return df


# ------------------------------------------------------------------ e-Conomy SEA
def fetch_econsea_pdfs():
    """Download the e-Conomy SEA report PDFs (2021-2025 editions). Returns {year: path}."""
    out = {}
    for y, url in ECONSEA_REPORTS.items():
        f = _path("econsea", f"e_conomy_sea_{y}.pdf")
        if not f.exists():
            r = _get(url, timeout=300)
            if r.status_code == 200 and r.content[:4] == b"%PDF":
                f.write_bytes(r.content)
        if f.exists():
            out[y] = f
    return out


# ------------------------------------------------------------------ OxCGRT (COVID restrictions)
def fetch_oxcgrt():
    """Oxford COVID-19 Government Response Tracker, daily, filtered to SEA + origin countries."""
    f = _path("oxcgrt", "oxcgrt_sea.parquet")
    if f.exists():
        return pd.read_parquet(f)
    r = _get(OXCGRT_URL, timeout=300)
    d = pd.read_csv(io.StringIO(r.text), low_memory=False)
    d = d[d.CountryCode.isin(list(COUNTRIES) + list(ORIGINS))]
    keep = ["CountryCode", "Date", "StringencyIndex_Average", "GovernmentResponseIndex_Average"]
    d = d[[c for c in keep if c in d.columns]]
    d.to_parquet(f)
    return d


# ------------------------------------------------------------------ CoinGecko (crypto ecosystem)
def fetch_coingecko_exchanges():
    """Every exchange CoinGecko tracks, with headquarters country, founding year and 24h volume.
    A snapshot of today (free API), used for crypto firm formation by country."""
    f = _path("coingecko", "exchanges.parquet")
    if f.exists():
        return pd.read_parquet(f)
    rows, page = [], 1
    while True:
        r = _get("https://api.coingecko.com/api/v3/exchanges", params={"per_page": 250, "page": page})
        batch = r.json()
        if not isinstance(batch, list) or not batch:
            break
        rows += batch
        page += 1
        time.sleep(8)                                   # free tier: keep well under the rate limit
    df = pd.DataFrame(rows)
    df = df[[c for c in ["id", "name", "country", "year_established", "trust_score",
                         "trade_volume_24h_btc", "trade_volume_24h_btc_normalized"] if c in df.columns]]
    df.to_parquet(f)
    return df


# ------------------------------------------------------------------ GDELT (news attention)
def fetch_gdelt_timeline(query, name, start="20170101000000"):
    """News volume for a query via the GDELT DOC 2.0 API (paced at 1 request / 6 s).
    The DOC API only covers 2017 onward."""
    f = _path("gdelt", f"{name}.json")
    if f.exists():
        return json.loads(f.read_text())
    time.sleep(6)
    r = _get("https://api.gdeltproject.org/api/v2/doc/doc",
             params={"query": query, "mode": "timelinevolraw", "format": "json", "startdatetime": start})
    try:
        data = r.json()
    except ValueError:
        data = {"error": r.text[:300]}
    f.write_text(json.dumps(data))
    return data


# ------------------------------------------------------------------ Reachability check
def http_status(url):
    """Status code and content type of a landing page, for sources that need manual collection."""
    try:
        r = S.get(url, timeout=45, allow_redirects=True, stream=True)
        r.close()
        return r.status_code, r.headers.get("Content-Type", "").split(";")[0]
    except requests.RequestException as e:
        return None, type(e).__name__


FETCHERS = {"worldbank": fetch_worldbank, "imf_fas": fetch_imf_fas, "imf_weo": fetch_imf_weo_gdp, "econsea": fetch_econsea_pdfs,
            "oxcgrt": fetch_oxcgrt, "coingecko": fetch_coingecko_exchanges}

if __name__ == "__main__":
    FETCHERS[sys.argv[1]]()
    print(f"[{sys.argv[1]}] done", flush=True)
