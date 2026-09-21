#!/usr/bin/env python3
"""
Rebuild data/tracker.json for the Insider Tape.

Two independent sources. Either can fail without taking the page down:

  1. Insider buys  — SEC EDGAR daily index -> Form 4 XML. Official, primary.
  2. Congress      — third-party parsed STOCK Act datasets. See CONGRESS_SOURCES.
                     The originals are PDFs, so a parsed feed is the only
                     practical route. If it dies, swap the URL, the page keeps
                     working and says the source is unavailable.

Stdlib only, so GitHub Actions needs no install step.

Run locally:   python3 scripts/update_tracker.py
Sample mode:   python3 scripts/update_tracker.py --sample
"""

import argparse
import concurrent.futures
import datetime as dt
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET

# SEC requires a descriptive User-Agent with contact info on every request.
# Set TRACKER_UA as a repo secret or edit the fallback. Requests without one
# get rate limited or blocked outright.
USER_AGENT = os.environ.get("TRACKER_UA", "Off-Script Rich tracker (contact@offscriptrich.com)")

SEC_BASE = "https://www.sec.gov/Archives/edgar/daily-index"
SEC_ARCHIVE = "https://www.sec.gov/Archives/"

# Both free, no API key. Bargo covers House + Senate and is current; LuxAlgo is
# a CC0 static dump on GitHub, used only if Bargo is down or returns nothing.
# Entries are (source_label, url) — chamber now comes from the record itself.
CONGRESS_SOURCES = [
    ("bargo", "https://www.bargo.ai/free-apis/congress/v1/trades?limit=500"),
    ("luxalgo", "https://raw.githubusercontent.com/LuxAlgo/market-trackers-data/main/congress/trades/latest.json"),
]

LOOKBACK_DAYS = 7           # trailing window for insider filings
CONGRESS_WINDOW_DAYS = 14   # trailing window on the DISCLOSURE date
MAX_FILINGS = 4000          # hard ceiling on Form 4 fetches per run
MAX_ROWS = 25               # rows rendered per table
WORKERS = 8
REQ_PER_SEC = 8.0           # stay well inside SEC's 10/sec guidance

OUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "tracker.json")


# ----------------------------------------------------------------- transport

class RateLimiter:
    """Simple global throttle shared across worker threads."""

    def __init__(self, per_sec):
        self._interval = 1.0 / per_sec
        self._lock = threading.Lock()
        self._next = 0.0

    def wait(self):
        with self._lock:
            now = time.monotonic()
            if now < self._next:
                time.sleep(self._next - now)
                now = time.monotonic()
            self._next = now + self._interval


LIMITER = RateLimiter(REQ_PER_SEC)


def get(url, timeout=30, retries=3, throttle=True):
    """GET returning bytes, or None if it never succeeded."""
    for attempt in range(retries):
        if throttle:
            LIMITER.wait()
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept-Encoding": "gzip, deflate",
                "Accept": "*/*",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read()
                if resp.headers.get("Content-Encoding") == "gzip":
                    import gzip
                    raw = gzip.decompress(raw)
                return raw
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None          # missing index day, not an error
            if e.code in (429, 503):
                time.sleep(2 ** attempt)
                continue
            return None
        except Exception:
            time.sleep(1 + attempt)
    return None


# ------------------------------------------------------------ insider buying

def business_days(end, count):
    """The `count` most recent weekdays, ending at `end` inclusive."""
    days, cur = [], end
    while len(days) < count:
        if cur.weekday() < 5:
            days.append(cur)
        cur -= dt.timedelta(days=1)
    return days


def daily_index_urls(days):
    for d in days:
        quarter = (d.month - 1) // 3 + 1
        yield d, "%s/%d/QTR%d/master.%s.idx" % (SEC_BASE, d.year, quarter, d.strftime("%Y%m%d"))


def collect_form4_paths(days):
    """Pull the daily master index for each day and return Form 4 archive paths."""
    paths = []
    for day, url in daily_index_urls(days):
        raw = get(url)
        if not raw:
            print("  no index for %s" % day.isoformat(), file=sys.stderr)
            continue
        text = raw.decode("latin-1", errors="replace")
        found = 0
        for line in text.splitlines():
            # CIK|Company Name|Form Type|Date Filed|Filename
            parts = line.split("|")
            if len(parts) != 5:
                continue
            if parts[2].strip() != "4":
                continue
            paths.append(parts[4].strip())
            found += 1
        print("  %s: %d form 4s" % (day.isoformat(), found), file=sys.stderr)
    # de-dupe, keep order
    seen, out = set(), []
    for p in paths:
        if p not in seen:
            seen.add(p)
            out.append(p)
    return out


OWNERSHIP_RE = re.compile(rb"<ownershipDocument>.*?</ownershipDocument>", re.DOTALL | re.IGNORECASE)


def _txt(node, path, default=""):
    """Form 4 wraps most leaves in a <value> child, sometimes not."""
    el = node.find(path)
    if el is None:
        return default
    v = el.find("value")
    target = v if v is not None else el
    return (target.text or "").strip() if target.text else default


def _num(node, path):
    raw = _txt(node, path)
    if not raw:
        return None
    try:
        return float(raw.replace(",", "").replace("$", ""))
    except ValueError:
        return None


def parse_form4(raw, archive_path):
    """Return a list of open-market purchase rows from one Form 4 submission."""
    if not raw:
        return []
    m = OWNERSHIP_RE.search(raw)
    if not m:
        return []
    try:
        doc = ET.fromstring(m.group(0))
    except ET.ParseError:
        return []

    issuer = doc.find("issuer")
    if issuer is None:
        return []
    company = _txt(issuer, "issuerName") or "unknown issuer"
    ticker = (_txt(issuer, "issuerTradingSymbol") or "").upper()
    if ticker in ("NONE", "N/A", "-"):
        ticker = ""

    owner = doc.find("reportingOwner")
    name, role = "unknown", ""
    if owner is not None:
        name = _txt(owner, "reportingOwnerId/rptOwnerName") or "unknown"
        rel = owner.find("reportingOwnerRelationship")
        if rel is not None:
            title = _txt(rel, "officerTitle")
            bits = []
            if title:
                bits.append(title)
            elif _txt(rel, "isOfficer") in ("1", "true"):
                bits.append("officer")
            if _txt(rel, "isDirector") in ("1", "true"):
                bits.append("director")
            if _txt(rel, "isTenPercentOwner") in ("1", "true"):
                bits.append("10% owner")
            role = ", ".join(bits)

    name = " ".join(w.capitalize() if w.isupper() and len(w) > 2 else w for w in name.split())

    rows = []
    table = doc.find("nonDerivativeTable")
    if table is None:
        return []
    for txn in table.findall("nonDerivativeTransaction"):
        code = _txt(txn, "transactionCoding/transactionCode").upper()
        if code != "P":                       # P = open-market purchase only
            continue
        ad = _txt(txn, "transactionAmounts/transactionAcquiredDisposedCode").upper()
        if ad and ad != "A":                  # A = acquired
            continue
        shares = _num(txn, "transactionAmounts/transactionShares")
        price = _num(txn, "transactionAmounts/transactionPricePerShare")
        if not shares or not price or price <= 0:
            continue
        rows.append({
            "ticker": ticker,
            "company": company.title() if company.isupper() else company,
            "insider": name,
            "role": role.lower(),
            "shares": int(shares),
            "price": round(price, 4),
            "value": int(round(shares * price)),
            "transaction_date": _txt(txn, "transactionDate"),
            "filed_date": "",
            "direction": "buy",
            "source_url": SEC_ARCHIVE + archive_path,
        })
    return rows


def fetch_insider_buys(days):
    paths = collect_form4_paths(days)
    if not paths:
        return None, 0
    if len(paths) > MAX_FILINGS:
        print("  capping at %d of %d filings" % (MAX_FILINGS, len(paths)), file=sys.stderr)
        paths = paths[:MAX_FILINGS]

    print("  fetching %d form 4s" % len(paths), file=sys.stderr)
    rows = []

    def work(p):
        return parse_form4(get(SEC_ARCHIVE + p, timeout=25, retries=2), p)

    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for i, result in enumerate(pool.map(work, paths)):
            rows.extend(result)
            if i and i % 500 == 0:
                print("    %d/%d" % (i, len(paths)), file=sys.stderr)

    return rows, len(paths)


def merge_same_filing(rows):
    """One insider buying across several tranches on a day is one purchase."""
    bucket = {}
    for r in rows:
        key = (r["ticker"], r["insider"], r["transaction_date"])
        if key in bucket:
            b = bucket[key]
            b["shares"] += r["shares"]
            b["value"] += r["value"]
        else:
            bucket[key] = dict(r)
    return list(bucket.values())


# ------------------------------------------------------------------ congress

def parse_amount_range(text):
    if not text:
        return None, None
    nums = re.findall(r"[\d,]+", text.replace("$", ""))
    vals = []
    for n in nums:
        try:
            vals.append(int(n.replace(",", "")))
        except ValueError:
            pass
    if not vals:
        return None, None
    if len(vals) == 1:
        return vals[0], vals[0]
    return min(vals), max(vals)


def parse_date(text):
    if not text:
        return None
    text = str(text).strip()
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%d %B %Y"):
        try:
            return dt.datetime.strptime(text[:10] if fmt == "%Y-%m-%d" else text, fmt).date()
        except ValueError:
            continue
    return None


def _cdate(v):
    """Dates arrive as '2026-09-02' or '2026-09-02T14:11:00Z'. Trim and parse."""
    if not v:
        return None
    return parse_date(str(v)[:10])


def _dig(rec, *names, **kw):
    """First non-empty value among several possible field names."""
    for n in names:
        if n in rec and rec[n] not in (None, ""):
            return rec[n]
    return kw.get("default")


def _congress_records(data):
    """Accept a bare array or an object wrapping the rows."""
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("data", "trades", "results", "records", "items", "rows"):
            v = data.get(key)
            if isinstance(v, list):
                return v
    return []


def _normalize_congress(rec, source):
    """Flatten Bargo / LuxAlgo / legacy shapes into one flat dict."""
    member = _dig(rec, "representative", "senator", "member", "name")
    state = _dig(rec, "state", default="")
    chamber = _dig(rec, "chamber", default="")
    if isinstance(member, dict):                  # luxalgo nests the member
        state = member.get("state") or state
        member = member.get("name") or member.get("fullName") or "unknown"

    amount = _dig(rec, "amount", "amount_range", "amountRange")
    lo = hi = None
    if isinstance(amount, dict):                  # luxalgo: {"min":.., "max":.., "text":..}
        lo, hi = amount.get("min"), amount.get("max")
        amount = amount.get("text") or amount.get("label")
    if lo is None and hi is None:
        lo, hi = _dig(rec, "amount_low"), _dig(rec, "amount_high")
    if lo is None and hi is None and amount:
        lo, hi = parse_amount_range(amount)

    return {
        "member": str(member or "unknown").strip(),
        "chamber": str(chamber or source).strip().lower(),
        "state": str(state or "").strip(),
        "ticker": str(_dig(rec, "ticker", "symbol", default="") or "").strip().upper(),
        "asset": str(_dig(rec, "asset_description", "asset", "assetDescription", default="") or "").strip(),
        "type": str(_dig(rec, "type", "transaction_type", "side", "action", default="") or "").lower(),
        "disclosed": _cdate(_dig(rec, "disclosure_date", "disclosed_date", "filedAt", "filed_at")),
        "traded": _cdate(_dig(rec, "transaction_date", "transactedAt", "transacted_at", "traded_at")),
        "amount_low": lo,
        "amount_high": hi,
    }


def fetch_congress(today):
    cutoff = today - dt.timedelta(days=CONGRESS_WINDOW_DAYS)
    out, any_ok, seen = [], False, set()

    for source, url in CONGRESS_SOURCES:
        raw = get(url, timeout=60, retries=2, throttle=False)
        if not raw:
            print("  congress source unavailable: %s" % source, file=sys.stderr)
            continue
        try:
            data = json.loads(raw.decode("utf-8", errors="replace"))
        except ValueError:
            print("  congress source unparseable: %s" % source, file=sys.stderr)
            continue

        records = _congress_records(data)
        if not records:
            print("  congress source returned no rows: %s" % source, file=sys.stderr)
            continue
        any_ok = True

        kept = 0
        for rec in records:
            if not isinstance(rec, dict):
                continue
            r = _normalize_congress(rec, source)

            if not r["disclosed"] or r["disclosed"] < cutoff or r["disclosed"] > today:
                continue
            if "purchase" not in r["type"] and "buy" not in r["type"]:
                continue

            ticker = r["ticker"]
            if ticker in ("--", "N/A", "NONE"):
                ticker = ""

            key = (r["member"].lower(), ticker,
                   r["traded"].isoformat() if r["traded"] else "", r["amount_high"])
            if key in seen:
                continue
            seen.add(key)

            out.append({
                "member": r["member"],
                "chamber": r["chamber"],
                "state": r["state"],
                "ticker": ticker,
                "company": (r["asset"] or ticker or "undisclosed asset")[:70],
                "type": "purchase",
                "amount_low": r["amount_low"],
                "amount_high": r["amount_high"],
                "transaction_date": r["traded"].isoformat() if r["traded"] else None,
                "disclosed_date": r["disclosed"].isoformat(),
                "lag_days": (r["disclosed"] - r["traded"]).days if r["traded"] else None,
            })
            kept += 1

        print("  %s: %d records, %d purchases in window" % (source, len(records), kept), file=sys.stderr)
        if kept:
            break

    if not any_ok:
        return None

    out.sort(key=lambda r: (r["amount_high"] or 0), reverse=True)
    return out


# --------------------------------------------------------------------- build

def build(sample=False):
    today = dt.date.today()

    if sample:
        print("sample mode: writing placeholder data", file=sys.stderr)
        payload = {
            "status": "sample",
            "generated_at": None,
            "period": {"from": (today - dt.timedelta(days=7)).isoformat(), "to": today.isoformat()},
            "sources": {"insider": "sample", "congress": "sample"},
            "totals": {"insider_buy_value": 0, "form4_purchase_filings": 0, "largest_buy": {"value": None, "who": None}},
            "insider_buys": [],
            "congress_trades": [],
        }
        write(payload)
        return 0

    days = business_days(today, LOOKBACK_DAYS)
    window_from = min(days)

    print("insider: scanning %s to %s" % (window_from.isoformat(), today.isoformat()), file=sys.stderr)
    insider_rows, scanned = fetch_insider_buys(days)

    insider_status = "ok"
    if insider_rows is None:
        insider_status = "failed"
        insider_rows = []
    else:
        insider_rows = merge_same_filing(insider_rows)
        insider_rows.sort(key=lambda r: r["value"], reverse=True)

    total_value = sum(r["value"] for r in insider_rows)
    largest = insider_rows[0] if insider_rows else None

    print("congress: pulling disclosures", file=sys.stderr)
    congress_rows = fetch_congress(today)
    congress_status = "ok" if congress_rows is not None else "failed"
    congress_rows = congress_rows or []

    payload = {
        "status": "live" if (insider_status == "ok" or congress_status == "ok") else "failed",
        "generated_at": dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat(),
        "period": {"from": window_from.isoformat(), "to": today.isoformat()},
        "sources": {"insider": insider_status, "congress": congress_status},
        "totals": {
            "insider_buy_value": total_value,
            "form4_purchase_filings": len(insider_rows),
            "form4_scanned": scanned,
            "largest_buy": {
                "value": largest["value"] if largest else None,
                "who": ("%s, %s, %s" % (largest["insider"], largest["role"] or "insider", largest["company"])).lower() if largest else None,
            },
        },
        "insider_buys": insider_rows[:MAX_ROWS],
        "congress_trades": congress_rows[:MAX_ROWS],
    }

    write(payload)

    print("done: %d insider purchases ($%s), %d congress purchases"
          % (len(insider_rows), "{:,}".format(total_value), len(congress_rows)), file=sys.stderr)

    # Fail the Actions run loudly if BOTH sources broke, so a silent stale
    # page is impossible. One source down is tolerated.
    if insider_status == "failed" and congress_status == "failed":
        print("ERROR: both sources failed, tracker.json not refreshed with real data", file=sys.stderr)
        return 1
    return 0


def write(payload):
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("wrote %s" % OUT_PATH, file=sys.stderr)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true", help="write an empty sample payload and exit")
    args = ap.parse_args()
    sys.exit(build(sample=args.sample))
