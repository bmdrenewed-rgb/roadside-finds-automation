#!/usr/bin/env python3
"""Roadside Finds: Wikimedia Commons discovery prototype.

Queries the Wikimedia Commons API for file search results and extracts
metadata for review-only purposes.  Never downloads or publishes files.

Usage:
    python commons_discovery.py
    python commons_discovery.py --query "construction" --limit 10
    python commons_discovery.py --output results.json
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

USER_AGENT = (
    "RoadsideFindsResearch/0.1 (non-commercial research; "
    "contact: repository owner via GitHub)"
)
API_BASE = "https://commons.wikimedia.org/w/api.php"
TIMEOUT = 30


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
    """Return a clean dict from an imageinfo api query result."""
    if not imginfo:
        return {}
    entry = imginfo[0] if isinstance(imginfo, list) else imginfo
    mime = entry.get("mime", "")
    dimensions = entry.get("imageinfo", [{}])[0].get("dimensions", {})
    return {
        "mime": mime,
        "width": dimensions.get("width"),
        "height": dimensions.get("height"),
        "size": entry.get("size"),           # file size in bytes
        "timestamp": entry.get("timestamp"),
        "user": entry.get("user"),
    }


def _parse_extmetadata(extmeta: List[Dict]) -> Dict[str, str]:
    """Extract key metadata fields from the extmetadata array."""
    meta: Dict[str, Any] = {}
    if not isinstance(extmeta, list):
        return meta
    for item in extmeta:
        key = item.get("name", "")
        value = _strip_html(item.get("value", ""))
        meta[key] = value
    return meta


def _build_record(
    page: Dict[str, Any],
    image_info: Dict[str, Any],
    extmetadata: Dict[str, str],
) -> Dict[str, Any]:
    """Build a single output record."""
    title = page.get("title", "")
    ns = page.get("ns", 0)

    # Direct file URL
    filename = page.get("title", "")
    if ns == 6:  # File namespace on Commons
        file_url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{urllib.parse.quote(filename)}"
    else:
        file_url = ""

    # Description page URL
    desc_url = f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(filename)}"

    return {
        "title": title,
        "description_url": desc_url,
        "file_url": file_url,
        "review_required": True,
        "license_verified": False,
        "mime": image_info.get("mime", ""),
        "width": image_info.get("width"),
        "height": image_info.get("height"),
        "size": image_info.get("size"),
        "upload_timestamp": image_info.get("timestamp"),
        "uploader": image_info.get("user", ""),
        "metadata": {
            "Artist": _strip_html(extmetadata.get("Artist")),
            "Credit": _strip_html(extmetadata.get("Credit")),
            "LicenseName": _strip_html(extmetadata.get("LicenseName")),
            "LicenseShortName": _strip_html(extmetadata.get("LicenseShortName")),
            "LicenseUrl": _strip_html(extmetadata.get("LicenseUrl")),
            "UsageTerms": _strip_html(extmetadata.get("UsageTerms")),
            "AttributionRequired": _strip_html(extmetadata.get("AttributionRequired")),
            "AttributionName": _strip_html(extmetadata.get("AttributionName")),
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Roadside Finds – Wikimedia Commons discovery prototype."
    )
    parser.add_argument(
        "--query",
        default="truck",
        help="Search term for Commons files (default: truck)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Maximum number of results (default: 5)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional path to write JSON output",
    )
    args = parser.parse_args()

    # Step 1: search
    search_params = {
        "action": "query",
        "list": "search",
        "srsearch": args.query,
        "srlimit": args.limit,
        "srnamespace": "6",  # File namespace only
        "format": "json",
    }
    search_data = _fetch(search_params)
    pages = search_data.get("query", {}).get("search", [])
    if not pages:
        print(json.dumps({"message": "no results found", "query": args.query}, indent=2))
        return

    titles = [p["title"] for p in pages]
    # Step 2: imageinfo + extmetadata
    imginfo_params = {
        "action": "query",
        "titles": "|".join(titles),
        "prop": "imageinfo|extmetadata",
        "iiprop": "mime|size|sha1|timestamp|user|dimensions",
        "eeprop": "Artist|Credit|LicenseName|LicenseShortName|LicenseUrl|UsageTerms|AttributionRequired|AttributionName",
        "format": "json",
    }
    imginfo_data = _fetch(imginfo_params)

    records: List[Dict[str, Any]] = []
    pages_dict = imginfo_data.get("query", {}).get("pages", {})
    for page in pages:
        title = page["title"]
        page_obj = pages_dict.get(str(title))  # API uses numeric page IDs
        # Find the matching page by title
        matching_page = None
        for pid, pobj in pages_dict.items():
            if pobj.get("title") == title:
                matching_page = pobj
                break
        if not matching_page:
            continue
        imginfo = matching_page.get("imageinfo", [])
        extmeta = matching_page.get("extmetadata", [])
        rec = _build_record(
            matching_page,
            _parse_image_info(imginfo),
            _parse_extmetadata(extmeta),
        )
        records.append(rec)

    output = {"query": args.query, "count": len(records), "records": records}
    json_str = json.dumps(output, indent=2, ensure_ascii=False)

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(json_str + "\n")
            print(f"[ok] written to {args.output}")
        except OSError as exc:
            print(f"[error] cannot write {args.output}: {exc}", file=sys.stderr)
            json_str  # fall through to stdout
    print(json_str)


if __name__ == "__main__":
    main()
