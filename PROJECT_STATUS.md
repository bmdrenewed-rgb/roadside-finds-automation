# Project Status: Roadside Finds

## Verified Commits (Already in History)

| # | Commit SHA | File | Description |
|---|------------|------|-------------|
| 1 | `4d430ce` | `.gitignore` | Initial commit: gitignore (secrets, venv, media, caches) |
| 2 | `b8eb3b7` | `README.md` | Initial commit: project scope, principles, installation |
| 3 | `9f1203e` | `requirements.txt` | Initial commit: `requests` dependency |
| 4 | `69745ce` | `README.md` | Updated: added script usage instructions and review-only limitations |
| 5 | `08bf583` | `commons_discovery.py` | Added: Wikimedia Commons discovery prototype script |

## Imageinfo API Documentation

The Imageinfo API endpoint (`prop=imageinfo`) was checked at:
https://www.mediawiki.org/wiki/API:Imageinfo

Key parameters used in this prototype:
- `iiprop=mime|size|sha1|timestamp|user|dimensions` — requested fields
- `eeprop=Artist|Credit|LicenseName|LicenseShortName|LicenseUrl|UsageTerms|AttributionRequired|AttributionName` — metadata fields
- `format=json` — JSON output format

The API returns structured JSON with no HTML, making metadata parsing safe.

## Prototype: `commons_discovery.py`

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

### What It Does NOT Do
- Does NOT verify legal permission to use any file.
- Does NOT download images or other media.
- Does NOT publish to any platform (TikTok, Metricool, etc.).
- Does NOT configure or store any secrets, tokens, or credentials.

## Next Tasks

1. Test against live Commons API with various search terms.
2. Inspect licenses individually for a subset of results.
3. Add unit tests for `commons_discovery.py`.
4. Build video editing pipeline for verified content.

## Security Note

- No posts to TikTok have been made.
- No credentials, tokens, or secrets exist in this repository.
- All assets require manual review before any use.
