# DISCOVERY STRATEGY

This document defines the topic buckets and relevance-exclusion rules for the
`commons_discovery.py` multi-topic video search pipeline.

## 1. Topic Buckets (Default Queries)

The seven default queries cover the following van-life video topic buckets:

| # | Query | Bucket |
|---|-------|--------|
| 1 | `"van life" filetype:video` | General van-life lifestyle & experience |
| 2 | `campervan conversion filetype:video` | Build / conversion documentation |
| 3 | `van build filetype:video` | Construction & fabrication processes |
| 4 | `van interior filetype:video` | Interiors, layouts, and storage solutions |
| 5 | `vanlife camping filetype:video` | Camping, campsite life, and on-the-road stops |
| 6 | `off-grid van solar filetype:video` | Off-grid power, solar setups, and energy independence |
| 7 | `vehicle dwelling filetype:video` | Broader vehicle-dwelling / nomadic-living content |

## 2. Relevance Exclusions

The following content types are explicitly excluded from the target niche.
Any matches that fall into these categories should be discarded during review:

1. **Commercial vans without living context** — delivery, ambulance, police, or other work-use vans not connected to a van-life narrative.
2. **Transit buses** — city buses, shuttle buses, and school buses.
3. **Trains / rail bogies / locomotives** — any rail-related content.
4. **Ordinary freight trucking** — semis, box trucks, or general cargo transport not directly part of a van-life story.
5. **Political or military material** — unless the content is directly relevant to van-life and has been cleared by legal review.
6. **Non-video file types** — the script filters to `media_type == "video"` and `mime.startswith("video/")` at the API level; non-video results are never included in output.

## 3. Safeguards

- **Review-only:** Every record carries `review_required=true`, `license_verified=false`, `approved_for_use=false`.
- **No downloading or publishing:** The script never downloads files or publishes content to any platform.
- **API metadata is a lead, not legal clearance:** Presence of metadata fields (Artist, LicenseName, etc.) does **not** constitute proof of legal permission to use a file. Each asset must be reviewed individually.
- **approved_records is always 0 at script exit:** The script sets `approved_records=0` in the top-level output. Approval is a manual process outside the scope of this tool.
- **No accounts created, no credentials committed.**

## 4. Deduplication

When multiple queries match the same file, only the **first** occurrence (by query order) is retained. Deduplication is by title.

## 5. File Structure

```
roadside-finds-automation/
├── commons_discovery.py    # Multi-topic VIDEO discovery script
├── DISCOVERY_STRATEGY.md   # This file — topic buckets & exclusions
├── LICENSE_REVIEW.md       # License review guidance
├── PROJECT_STATUS.md       # Project milestones & status
├── README.md               # Project overview & usage
└── requirements.txt        # (empty — script is dependency-free)
```
