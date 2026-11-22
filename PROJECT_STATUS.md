Project Status: Roadside Finds
==============================

User Correction: Niche Redirection
-----------------------------------

The target niche has been corrected from **trucking/trucker content** to **VAN LIFE** (vehicle-dwelling discoveries).

**New scope:** Van life, campervan/RV builds and conversions, interiors and layouts, compact storage/organization, off-grid power and solar, cooking and daily routines on the road, campsites/roadside stops, travel routes/scenery, practical gear, budget/DIY solutions, and real van-life experiences.

**Clarification:** Trucks or semis are only relevant if directly part of a van-life story — they are NOT the target on their own.

Discovery Priorities (Updated for Van Life)
--------------------------------------------

1. Search Wikimedia Commons using van-life terms: `van life`, `campervan conversion`, `van build`, `van interior`, `vanlife camping`, `off-grid van solar`, `vehicle dwelling`
2. Improve query relevance with van-life-specific keywords and Commons categories
3. Improve metadata extraction (dimensions/width/height)
4. Inspect licenses individually
5. Test the script itself (automated edge-case testing)
6. Build a structured review queue for assets
7. Create a video from **only** an approved asset

Verified Commits (Already in History)
-------------------------------------

| # | Commit SHA | File | Description |
| --- | --- | --- | --- |
| 1 | `4d430ce` | `.gitignore` | Initial commit: gitignore (secrets, venv, media, caches) |
| 2 | `b8eb3b7` | `README.md` | Initial commit: project scope, principles, installation |
| 3 | `9f1203e` | `requirements.txt` | Initial commit: `requests` dependency |
| 4 | `69745ce` | `README.md` | Updated: added script usage instructions and review-only limitations |
| 5 | `08bf583` | `commons_discovery.py` | Added: Wikimedia Commons discovery prototype script |

Prior Truck Search Results Are Not Relevant Validation
------------------------------------------------------

**The prior live discovery test using `filetype:video truck` is NOT relevant validation for the van-life niche.** The keyword `truck` matched irrelevant content (railway bogie trucks, military content, protest footage). Those results should not be considered evidence that van-life assets are unavailable.

**Current status: Still 0 assets approved for the van-life niche.** We need fresh discovery results using van-life search terms.

Live Discovery Test Results (Van Life)
--------------------------------------

A live API test was conducted on **2026-11-22** using the search term `filetype:video van life`.

| Metric | Value |
| --- | --- |
| Results Returned | 5 |
| Results Approved | 0 |
| File Format | WebM / various |
| Dimensions Available | Vary by result |

**Key Discovery:** The original `truck` query was too broad and irrelevant. Updated to `van life` and related van-life terms for proper niche alignment.

Prototype: commons_discovery.py
--------------------------------

### What It Does

* Queries Wikimedia Commons API for file search results (default: search term "van life", 5 results).
* Extracts: title, description page URL, direct file URL, MIME type, dimensions, file size, upload timestamp, uploader.
* Extracts extended metadata: Artist, Credit, LicenseName, LicenseShortName, LicenseUrl, UsageTerms, AttributionRequired, AttributionName.
* Sets a descriptive User-Agent and a 30-second timeout.
* Handles API/network errors and missing metadata gracefully.
* Marks all records as `review_required=true` and `license_verified=false`.
* Never downloads or publishes files.
* Outputs JSON to stdout or an optional `--output` file path.

### What It Does Not Do

* Does NOT verify legal permission to use any file.
* Does NOT download images or other media.
* Does NOT publish to any platform (TikTok, Metricool, etc.).
* Does NOT configure or store any secrets, tokens, or credentials.
* Uses a single-query prototype (not multi-query).

Security Note
-------------

* No posts to TikTok have been made.
* No downloads of media have occurred.
* No credentials, tokens, or secrets exist in this repository.
* All assets require manual review before any use.
* **No asset has been approved for TikTok use.**
