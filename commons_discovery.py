#!/usr/bin/env python3
"""Roadside Finds: Wikimedia Commons multi-topic VIDEO discovery script.

Queries the Wikimedia Commons API for file search results across multiple
van-life video topic buckets and extracts metadata for review-only purposes.
Never downloads or publishes files.

Usage:

    # Run with all 7 default queries:
    python commons_discovery.py

    # Replace defaults with custom queries:
    python commons_discovery.py --query "van life filetype:video" \\
                                 --query "campervan conversion filetype:video"

    # Set per-query limit (1-50, default 10):
    python commons_discovery.py --limit 25

    # Write JSON output:
    python commons_discovery.py --output results.json

Dependencies: Python standard library only + Wikimedia Commons API.

Safeguards:
    * Every record has review_required=True, license_verified=False,
      approved_for_use=False.
    * The script never downloads or publishes any asset.
    * API search metadata is a lead, not legal clearance.
"""
from __future__ import annotations

import argparse
import html
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
USER_AGENT = (
    "RoadsideFindsResearch/0.2 (non-commercial research; "
    "contact: repository owner via GitHub)"
)
API_BASE = "https://commons.wikimedia.org/w/api.php"
TIMEOUT = 30

DEFAULT_QUERIES: List[str] = [
    '"van life" filetype:video',
    'campervan conversion filetype:video',
    'van build filetype:video',
    'van interior filetype:video',
    'vanlife camping filetype:video',
    'off-grid van solar filetype:video',
    'vehicle dwelling filetype:video',
]

EXTMETA_FILTER = (
    "Artist|Credit|LicenseName|LicenseShortName|LicenseUrl|"
    "UsageTerms|AttributionRequired|AttributionName|ImageDescription"
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _fetch(params: Dict[str, str]) -> Dict[str, Any]:
    """Send a GET request to the Commons API and return parsed JSON."""
    url = API_BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        print(f"[error] HTTP {exc.code}: {exc.reason}", file=sys.stderr)
        return {}
    except urllib.error.URLError as exc:
        print(f"[error] URL error: {exc.reason}", file=sys.stderr)
        return {}
    except json.JSONDecodeError:
        print("[error] failed to decode JSON response", file=sys.stderr)
        return {}


def _strip_html(text: Optional[str]) -> str:
    """Safely strip HTML markup from a metadata value."""
    if not text:
        return ""
    return html.unescape(text)


# ---------------------------------------------------------------------------
# Extraction
# ---------------------------------------------------------------------------
def _parse_image_info(imginfo: Dict[str, Any]) -> Dict[str, Any]:
    """Return a clean dict from imageinfo API query result."""
    if not imginfo:
        return {}
    entry = imginfo[0] if isinstance(imginfo, list) else imginfo
    mime = entry.get("mime", "")
    dims = entry.get("dimensions", {})
    return {
        "mime": mime,
        "width": dims.get("width"),
        "height": dims.get("height"),
        "duration": entry.get("duration"),
        "size": entry.get("size"),
        "timestamp": entry.get("timestamp"),
        "user": entry.get("user"),
    }


def _parse_extmetadata(extmeta: List[Dict]) -> Dict[str, str]:
    """Extract key metadata fields from the extmetadata array."""
    meta: Dict[str, str] = {}
    if not isinstance(extmeta, list):
        return meta
    for item in extmeta:
        key = item.get("name", "")
        value = _strip_html(item.get("value", ""))
        meta[key] = value
    return meta


def _build_record(
    title: str,
    matched_query: str,
    image_info: Dict[str, Any],
    extmetadata: Dict[str, str],
) -> Dict[str, Any]:
    """Build a single output record."""
    # Direct file URL
    file_url = (
        f"https://commons.wikimedia.org/wiki/"
        f"Special:FilePath/{urllib.parse.quote(title)}"
    )
    # Description page URL
    desc_url = f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(title)}"
    return {
        "matched_query": matched_query,
        "title": title,
        "description_url": desc_url,
        "file_url": file_url,
        "mime": image_info.get("mime", ""),
        "width": image_info.get("width"),
        "height": image_info.get("height"),
        "duration": image_info.get("duration"),
        "size": image_info.get("size"),
        "upload_timestamp": image_info.get("timestamp"),
        "uploader": image_info.get("user", ""),
        "license_name": _strip_html(extmetadata.get("LicenseName")),
        "license_short_name": _strip_html(extmetadata.get("LicenseShortName")),
        "license_url": _strip_html(extmetadata.get("LicenseUrl")),
        "artist": _strip_html(extmetadata.get("Artist")),
        "credit": _strip_html(extmetadata.get("Credit")),
        "usage_terms": _strip_html(extmetadata.get("UsageTerms")),
        "attribution_required": _strip_html(
            extmetadata.get("AttributionRequired")
        ),
        "attribution_name": _strip_html(extmetadata.get("AttributionName")),
        "image_description": _strip_html(
            extmetadata.get("ImageDescription")
        ),
        "review_required": True,
        "license_verified": False,
        "approved_for_use": False,
    }


# ---------------------------------------------------------------------------
# Multi-topic discovery
# ---------------------------------------------------------------------------
def discover(queries: List[str], limit: int) -> Dict[str, Any]:
    """Run discovery for each query, deduplicate by title, and return output."""
    seen_titles: set = set()
    all_records: List[Dict[str, Any]] = []
    per_query_counts: List[Dict[str, Any]] = []

    for query in queries:
        # --- Step 1: search ---
        search_params: Dict[str, str] = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "srlimit": str(limit),
            "srnamespace": "6",  # File namespace only
            "format": "json",
        }
        search_data = _fetch(search_params)
        pages = search_data.get("query", {}).get("search", [])

        query_total = len(pages)
        query_video = 0

        if not pages:
            per_query_counts.append({
                "query": query,
                "total_hits": 0,
                "video_hits": 0,
                "skipped_duplicate": 0,
            })
            continue

        titles = [p["title"] for p in pages]

        # --- Step 2: imageinfo + extmetadata (batch by unique titles) ---
        unique_titles = list(dict.fromkeys(titles))  # preserve order, dedupe
        batch_size = 50
        batch_results: List[Dict[str, Any]] = []

        for i in range(0, len(unique_titles), batch_size):
            batch = unique_titles[i : i + batch_size]
            imginfo_params: Dict[str, str] = {
                "action": "query",
                "titles": "|".join(batch),
                "prop": "imageinfo|extmetadata",
                "iiprop": "url|mime|size|timestamp|user|dimensions|mediatype"
                          "|extmetadata|duration",
                "iiextmetadatafilter": EXTMETA_FILTER,
                "format": "json",
            }
            imginfo_data = _fetch(imginfo_params)
            pages_dict = imginfo_data.get("query", {}).get("pages", {})
            for pid, pobj in pages_dict.items():
                if pobj.get("ns") != 6:
                    continue
                batch_results.append(pobj)

        # --- Step 3: filter & build records ---
        for page in pages:
            title = page["title"]
            if title in seen_titles:
                continue

            matching_page = None
            for pobj in batch_results:
                if pobj.get("title") == title:
                    matching_page = pobj
                    break
            if not matching_page:
                continue

            imginfo = matching_page.get("imageinfo", [])
            extmeta = matching_page.get("extmetadata", [])

            # Parse image info
            info = _parse_image_info(imginfo)
            mime = info.get("mime", "")
            media_type = info.get("media_type", "")

            # Keep only VIDEO or mime starting with video/
            if media_type != "video" and not mime.startswith("video/"):
                continue

            seen_titles.add(title)
            query_video += 1

            record = _build_record(title, query, info, extmeta)
            all_records.append(record)

        per_query_counts.append({
            "query": query,
            "total_hits": query_total,
            "video_hits": query_video,
            "skipped_duplicate": len(titles) - len(
                [t for t in titles if t not in seen_titles]
            ),
        })

    # --- Build top-level output ---
    output = {
        "queries": queries,
        "per_query_counts": per_query_counts,
        "video_count": len(all_records),
        "approved_records": 0,
        "records": all_records,
        "notice": (
            "This output represents API search metadata only and is NOT "
            "legal clearance to use any file. Each asset must be reviewed "
            "individually for license compliance before any use."
        ),
    }
    return output


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Roadside Finds - Wikimedia Commons multi-topic VIDEO discovery. "
            "Deduplicates by title, filters to video media type only, and "
            "outputs JSON."
        ),
    )
    parser.add_argument(
        "--query",
        action="append",
        default=None,
        help=(
            'Search term for Commons files (can be repeated). '
            "If omitted, the 7 default van-life queries are used."
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=10,
        help="Max results per query (1-50, default: 10).",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to write JSON output.",
    )
    args = parser.parse_args()

    # Clamp limit
    if args.limit is None or args.limit > 50:
        args.limit = 50
    if args.limit is None or args.limit > 50:
        args.limit = 50
    if args.limit > 50:
        args.limit = 50
    if args.limit > 50:
        args.limit = 50
    if args.limit > 50:
        args.limit = 50
    queries = args.query if args.query else DEFAULT_QUERIES

    print(f"Running discovery with {len(queries)} query(ies)...")
    result = discover(queries, args.limit)

    json_str = json.dumps(result, indent=2, ensure_ascii=False)

    # Print per-query summary
    for qc in result["per_query_counts"]:
        print(
            f"  {qc['query']!r}  total={qc['total_hits']}  video={qc['video_hits']}"
        )
    print(
        f"\nTotal video records: {result['video_count']}  "
        f"approved: {result['approved_records']}"
    )
    print(f"[notice] {result['notice']}")

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(json_str + "\n")
            print(f"[ok] written to {args.output}")
        except OSError as exc:
            print(f"[error] cannot write {args.output}: {exc}", file=sys.stderr)

    print(json_str)


if __name__ == "__main__":
    main()
