Roadside Finds TikTok Automation
================================

Project Scope
-------------

This repository supports an automated workflow for **Roadside Finds**, a TikTok account (handle: `@RoadsideFinds`) that shares curated finds from the roadside. The goal is to discover interesting items, verify them, record their provenance, and schedule content for publication — all through a well-documented, repeatable process.

### Niche Definition: VAN LIFE

This project targets the **van-life** niche — content about people living in vans, campervans, and RVs. The channel focuses on vehicle-dwelling discoveries, not general trucking or trucker content.

**Van-life topics include:**

* Living in vans and campervans / RV builds and conversions
* Van interiors and layouts
* Compact storage and organization solutions
* Off-grid power and solar setups
* Cooking and daily routines on the road
* Campsites and roadside stops
* Travel routes and scenery
* Practical van-life gear
* Budget and DIY van-life solutions
* Real van-life experiences and stories

**Trucks and semis are NOT the target.** They are only relevant when they are directly part of a van-life story (e.g., a trucker sharing a roadside find, or a truck used in van-life travel).

### Core Principles

* **Safety First**: Only use individually verified, reusable assets (photos, clips, text snippets). Every asset must be traceable to its source before use.
* **Attribution Required**: For each asset, record:
  + Source URL
  + Creator name
  + License name
  + License URL
* **No Publishing Before Review**: All scheduled content must pass a manual review step before being posted to TikTok.
* **Never Commit Secrets**: Tokens, API keys, passwords, and credentials must never be committed to this repository. Use environment variables and `.env` files (which are gitignored).
* **Scheduler**: [Metricool](https://metricool.com/) is the intended scheduling tool for publishing content to TikTok on a consistent cadence.

### Account Details

| Field | Value |
| --- | --- |
| TikTok Account | RoadsideFinds |
| Timezone | America/New_York |

Getting Started
---------------

### Installation

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the Prototype

```
# Default search (van life) with 5 results
python commons_discovery.py

# Custom search term and limit
python commons_discovery.py --query "campervan conversion" --limit 10

# Example query terms for van-life content:
#   "van life", "campervan conversion", "van build", "van interior"
#   "vanlife camping", "off-grid van solar", "vehicle dwelling"

# Output to file
python commons_discovery.py --output results.json
```

### `commons_discovery.py`

This script queries the **Wikimedia Commons API** (`https://commons.wikimedia.org/w/api.php`) to search for files and extract metadata. It is a **research prototype only** with the following characteristics:

* **Review-only**: All records are marked `review_required=true` and `license_verified=false`. Metadata presence is **never** treated as proof of legal permission to use a file.
* **No downloading or publishing**: The script never downloads image files or publishes content to any platform.
* **What it extracts**: title, description page URL, direct file URL, MIME type, dimensions, file size, upload timestamp, uploader, and extensive metadata fields (Artist, Credit, LicenseName, LicenseShortName, LicenseUrl, UsageTerms, AttributionRequired, AttributionName).
* **Error handling**: Network and API errors are handled gracefully; missing metadata is reported as `null` rather than causing crashes.
* **Output**: JSON to stdout or an optional `--output` file path.

Live Discovery Test Results
---------------------------

A live API test was conducted on **2026-11-22** using the search term `filetype:video van life`.

| Metric | Value |
| --- | --- |
| Results Returned | 5 |
| Results Approved | 0 |
| File Format | WebM / various |
| Dimensions Available | Vary by result |

**Key Discovery:** The keyword `truck` was previously too broad and irrelevant to the target niche. The query has been updated to `van life` (and related van-life terms) to better match the channel's target audience.

Full review details are documented in [`LICENSE_REVIEW.md`](/bmdrenewed-rgb/roadside-finds-automation/blob/main/LICENSE_REVIEW.md).

### Updated Next Tasks

* Initial repository setup (README, .gitignore, requirements.txt)
* First prototype: `commons_discovery.py` — Wikimedia Commons discovery
* Test against live Commons API
* Improve query relevance with van-life-specific keywords
* Improve metadata/dimensions extraction
* Inspect licenses individually
* Add unit tests
* Build review queue for assets
* Build video editing pipeline
* Create a video from **only** an approved asset

License
-------

This project uses publicly licensed assets. Each asset's license is recorded in its metadata.
