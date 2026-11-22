# PROJECT STATUS

This document outlines the current status of the roadside finds automation project. It details the progress, upcoming milestones, and any identified issues or blockers.

## 1. Project Overview

The goal of this project is to automate the process of discovering and cataloging roadside finds using various data sources and machine learning techniques.

## 2. Current Status

- **Development:** Multi-topic `commons_discovery.py` script implementation is complete (v0.2). Runtime test is still pending.
- **Testing:** In progress. Initial testing of the discovery module has shown promising results.
- **Deployment:** N/A. Currently in the development phase.

## 3. Key Accomplishments

- Implemented API integration for [Wikimedia Commons](https://commons.wikimedia.org/).
- Developed a Python script (`commons_discovery.py`) to query the Wikimedia Commons API for relevant image files based on search queries.
- Established a data structure for storing extracted metadata.
- **2026-11-22:** Rewrote `commons_discovery.py` as a true multi-topic van-life VIDEO discovery script:
  - Seven default topic queries (see `DISCOVERY_STRATEGY.md`).
  - `--query` repetition to replace defaults.
  - `--limit 1-50` per query.
  - `--output` JSON path.
  - Deduplication by title across queries.
  - Filter to VIDEO media type only.
  - Extract extmetadata (Artist, Credit, LicenseName, etc.).
  - Every record carries `review_required=true`, `license_verified=false`, `approved_for_use=false`.
  - Output includes `per_query_counts`, `video_count`, `approved_records=0`, and a clear notice that search metadata is only a lead, not legal clearance.
- Updated README.md with multi-topic usage instructions and exact safeguards.
- Updated PROJECT_STATUS.md to reflect completion of multi-topic implementation and to record live search evidence.

## 4. Live Search Evidence (2026-11-22)

- A live search on Wikimedia Commons for the query `campervan conversion filetype:video` returned at least one relevant video file:
  - **`LDV Convoy 1996 400 series - Campervan conversion - Part 1.webm`** — This confirms that Commons does contain van-life / campervan conversion video content.
  - **IMPORTANT:** This is a *lead*, not an approved asset. No legal review has been performed.
- Additional image results were found for topics including solar van, van interiors, and campsite footage, but these are image files (not video) and should not be conflated with video results.

## 5. Upcoming Milestones

- **2026-11-22 (Current):**
  - [x] Multi-topic script implementation (complete).
  - [x] README.md updated with multi-topic usage and safeguards.
  - [x] DISCOVERY_STRATEGY.md created with topic buckets and exclusions.
  - [ ] Runtime test of `commons_discovery.py` against live Commons API (pending).
- **Q1 2027:**
  - Conduct runtime tests and validate extmetadata extraction.
  - Begin integration with a second data source (e.g., Flickr).
  - Develop a preliminary classification model for identified finds.
  - Conduct user acceptance testing.

## 6. Issues and Blockers

- **API Rate Limits:** Potential rate limiting from data sources needs to be monitored and handled gracefully.
- **Data Quality:** Variations in metadata quality across different sources require robust error handling and data cleaning.
- **Scalability:** As the project grows, ensuring the scalability of the data processing pipeline will be crucial.
- **Runtime test pending:** Multi-topic script has been implemented but has not yet been run end-to-end against live data.

## 7. Future Work

- Explore integration with more data sources.
- Enhance the machine learning models for improved classification and analysis.
- Develop a user-friendly interface for browsing and managing findings.
- Build a review queue for assets.
- Build a video editing pipeline.

## 8. Contributors

- [bmdrenewed-rgb](https://github.com/bmdrenewed-rgb)

## Last Updated: November 22, 2026
