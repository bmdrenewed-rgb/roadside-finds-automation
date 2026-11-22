# Roadside Finds TikTok Automation

## Project Scope

This repository supports an automated workflow for **Roadside Finds**, a TikTok account (handle: `@RoadsideFinds`) that shares curated finds from the roadside. The goal is to discover interesting items, verify them, record their provenance, and schedule content for publication — all through a well-documented, repeatable process.

### Core Principles

- **Safety First**: Only use individually verified, reusable assets (photos, clips, text snippets). Every asset must be traceable to its source before use.
- **Attribution Required**: For each asset, record:
  + Source URL
  + Creator name
  + License name
  + License URL
- **No Publishing Before Review**: All scheduled content must pass a manual review step before being posted to TikTok.
- **Never Commit Secrets**: Tokens, API keys, passwords, and credentials must never be committed to this repository. Use environment variables and `.env` files (which are gitignored).
- **Scheduler**: [Metricool](https://metricool.com/) is the intended scheduling tool for publishing content to TikTok on a consistent cadence.

### Account Details

| Field | Value |
|---|---|
| TikTok Account | RoadsideFinds |
| Timezone | America/New_York |

## Getting Started

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Running the Prototype

```bash
# Default search (truck) with 5 results
python commons_discovery.py

# Custom search term and limit
python commons_discovery.py --query "construction equipment" --limit 10

# Output to file
python commons_discovery.py --output results.json
```

### `commons_discovery.py`

This script queries the **Wikimedia Commons API** (`https://commons.wikimedia.org/w/api.php`) to search for files and extract metadata. It is a **research prototype only** with the following characteristics:

- **Review-only**: All records are marked `review_required=true` and `license_verified=false`. Metadata presence is **never** treated as proof of legal permission to use a file.
- **No downloading or publishing**: The script never downloads image files or publishes content to any platform.
- **What it extracts**: title, description page URL, direct file URL, MIME type, dimensions, file size, upload timestamp, uploader, and extensive metadata fields (Artist, Credit, LicenseName, LicenseShortName, LicenseUrl, UsageTerms, AttributionRequired, AttributionName).
- **Error handling**: Network and API errors are handled gracefully; missing metadata is reported as `null` rather than causing crashes.
- **Output**: JSON to stdout or an optional `--output` file path.

## Live Discovery Test Results

A live API test was conducted on **2026-11-22** using the search term `filetype:video truck`.

| Metric | Value |
|---|---|
| Results Returned | 5 |
| Results Approved | 0 |
| File Format | All WebM |
| Dimensions Available | None (missing from all results) |

**Key Discovery:** The keyword `truck` is too broad — it matches railway bogie trucks (irrelevant), politically sensitive protest footage (off-topic), and military content with unclear provenance. **Query relevance needs improvement.**

Full review details are documented in [`LICENSE_REVIEW.md`](LICENSE_REVIEW.md).

### Updated Next Tasks

- [x] Initial repository setup (README, .gitignore, requirements.txt)
- [x] First prototype: `commons_discovery.py` — Wikimedia Commons discovery
- [x] Test against live Commons API
- [ ] Improve query relevance (add specific keywords, use Commons categories)
- [ ] Improve metadata/dimensions extraction (dimensions/width/height were absent)
- [ ] Inspect licenses individually
- [ ] Add unit tests
- [ ] Build review queue for assets
- [ ] Build video editing pipeline
- [ ] Create a video from **only** an approved asset

## License

This project uses publicly licensed assets. Each asset's license is recorded in its metadata.
