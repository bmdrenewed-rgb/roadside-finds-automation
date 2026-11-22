# Project Status: Roadside Finds

## Verified Commits (Already in History)


| # | Commit SHA | File | Description |
|---|---|---|---|
| 1 | `4d430ce` | `.gitignore` | Initial commit: gitignore (secrets, venv, media, caches) |
| 2 | `b8eb3b7` | `README.md` | Initial commit: project scope, principles, installation |
| 3 | `9f1203e` | `requirements.txt` | Initial commit: `requests` dependency |
| 4 | `69745ce` | `README.md` | Updated: added script usage instructions and review-only limitations |
| 5 | `08bf583` | `commons_discovery.py` | Added: Wikimedia Commons discovery prototype script |

## Project Milestones

### Milestone 1: Live Wikimedia Commons API Discovery Test ✅

- **Date:** 2026-11-22
- **Action:** Ran live discovery test against Wikimedia Commons API using `filetype:video truck`
- **Results Returned:** 5
- **Results Approved:** 0
- **Full review documented in:** [`LICENSE_REVIEW.md`](LICENSE_REVIEW.md)

### Key Discovery: Keyword 'truck' is Too Broad

The term `truck` matches not only road vehicles but also:
- **Railway bogie trucks** (train cars) — irrelevant to Roadside Finds
- **Politically sensitive content** (protest footage) — off-topic
- **Military / defense content** — rights chain unclear (sourced from third-party YouTube)

This limitation means the basic keyword query needs refinement before being production-ready.

### Next Tasks for Discovery Pipeline

1. Improve query relevance (add more specific keywords, use Commons categories)
2. Improve metadata extraction (dimensions/width/height were absent from all 5 results)
3. Test the script itself (automated edge-case testing)
4. Build a structured review queue for assets
5. Create a video from **only** an approved asset

## Prototype: commons_discovery.py

### What It Does

- Queries Wikimedia Commons API for file search results (default: search term "truck", 5 results).
- Extracts: title, description page URL, direct file URL, MIME type, dimensions, file size, upload timestamp, uploader.
- Extracts extended metadata: Artist, Credit, LicenseName, LicenseShortName, LicenseUrl, UsageTerms, AttributionRequired, AttributionName.
- Parses HTML in metadata values safely using `html.unescape()`.
- Sets a descriptive User-Agent and a 30-second timeout.
- Handles API/network errors and missing metadata gracefully.
- Marks all records as `review_required=true` and `license_verified=false`.
- Never downloads or publishes files.
- Outputs JSON to stdout or an optional `--output` file path.

### What It Does Not Do

- Does NOT verify legal permission to use any file.
- Does NOT download images or other media.
- Does NOT publish to any platform (TikTok, Metricool, etc.).
- Does NOT configure or store any secrets, tokens, or credentials.

## Imageinfo API Documentation

- **Documentation URL:** [https://www.mediawiki.org/wiki/API:Imageinfo](https://www.mediawiki.org/wiki/API:Imageinfo)
- **Key parameters:**
  - `iiprop=mime|size|sha1|timestamp|user|dimensions`
  - `eeprop=Artist|Credit|LicenseName|LicenseShortName|LicenseUrl|UsageTerms|AttributionRequired|AttributionName`
  - `format=json`
- **Output format:** The API returns structured JSON with no HTML, making metadata parsing safe.

## Next Tasks

- [x] Initial repository setup (README, .gitignore, requirements.txt)
- [x] First prototype: `commons_discovery.py` — Wikimedia Commons discovery
- [x] Test against live Commons API
- [ ] Inspect licenses individually
- [ ] Add unit tests
- [ ] Build video editing pipeline

## Security Note

- No posts to TikTok have been made.
- No credentials, tokens, or secrets exist in this repository.
- All assets require manual review before any use.
- **No asset has been approved for TikTok use.**
