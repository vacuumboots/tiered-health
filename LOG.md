# Tiered Health — Session Log

## 2026-07-15 — Session 2 (batch deployment)
- Created kanban pilot task for ankle-sprain → worker completed in 4 min, 18KB content + 9KB SVG
- Batch-created 10 tasks via create-batch.sh: migraine, carpal-tunnel, sciatica, herniated-disc, gout, kidney-stones, UTI, plantar-fasciitis, sinusitis, GERD
- All 10 workers completed → 12 pages total (incl. radial-nerve-palsy + ankle-sprain)
- Fixed CSS: danger callout white-on-white in dark mode (hardcoded #fdf2f2 → var(--danger-light))
- Added accessibility: skip-to-content link, back-to-index, focus-visible styles
- Created project docs: TODO.md, LOG.md, USER_steps.md
- Created reusable skill: tiered-health-pipeline

## 2026-07-15 — Session 1 (pipeline build)
- Wrote concept page at ~/wiki/concepts/tiered-health-pages.md
- Built radial-nerve-palsy.html prototype: three tiers, SVG anatomy, tier toggle JS, dark mode
- Extracted build pipeline: template.html, build.py, content/*.md, svg/*.svg
- build.py features: YAML frontmatter parser, markdown→HTML (headings/lists/tables/callouts/timeline), SVG inlining, index generation with search
- Content format: `## ::gist::` / `::adult::` / `::full::` / `::timeline::` / `::sources::`
- Zero external dependencies (pure Python stdlib)
- Second session started around 00:30. Built pipeline, kanban pilot, batch.
