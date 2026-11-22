# Roadside Finds TikTok Automation

## Project Scope

This repository supports an automated workflow for **Roadside Finds**, a TikTok account (handle: `@RoadsideFinds`) that shares curated finds from the roadside. The goal is to discover interesting items, verify them, record their provenance, and schedule content for publication — all through a well-documented, repeatable process.

### Core Principles

- **Safety First**: Only use individually verified, reusable assets (photos, clips, text snippets). Every asset must be traceable to its source before use.
- **Attribution Required**: For each asset, record:
  - Source URL
  - Creator name
  - License name
  - License URL
- **No Publishing Before Review**: All scheduled content must pass a manual review step before being posted to TikTok.
- **Never Commit Secrets**: Tokens, API keys, passwords, and credentials must never be committed to this repository. Use environment variables and `.env` files (which are gitignored).
- **Scheduler**: [Metricool](https://metricool.com/) is the intended scheduling tool for publishing content to TikTok on a consistent cadence.

### Account Details

| Field | Value |
|-------|-------|
| TikTok Account | RoadsideFinds |
| Timezone | America/New_York |

## Getting Started

This is the initial commit. The first prototype focuses on **Wikimedia Commons discovery and metadata extraction** to identify publicly licensed images that may be suitable for the Roadside Finds feed.

### Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Dependencies

See `requirements.txt` for the minimal first-pass library.

## License

This project uses publicly licensed assets. Each asset's license is recorded in its metadata.
