# Tiered Health

One page per common injury or ailment. Three reading levels, visual anatomy diagrams, and current medical evidence — all in a self-contained HTML page.

**Live example:** [radial nerve palsy](https://github.com/vacuumboots/tiered-health) (Gist → Adult → Full)

## How it works

Every condition page has a toggle at the top:

| Tier | Reading level | What you get |
|------|---------------|--------------|
| **Gist** | Grade 6 | One sentence. What to do. When to go to the ER. ~80 words. |
| **Adult** | Grade 12 | Mechanism, symptoms, treatment options, recovery timeline, pitfalls. |
| **Full** | Best evidence | Pathophysiology, differential diagnosis, diagnostic workup, Cochrane reviews, surgical options, open research questions. |

Each page includes an SVG anatomy diagram showing the affected body part and a visual recovery timeline. Dark mode is automatic. Print shows all three tiers.

## Quick start

```bash
# Add a new condition
cp content/TEMPLATE.md content/your-condition.md   # fill it in
# Create svg/your-condition.svg
python3 build.py your-condition                     # → dist/your-condition.html
python3 build.py                                     # build all + index
open dist/index.html
```

**Zero dependencies.** `build.py` uses only Python stdlib. Converts markdown to HTML, inlines SVGs, renders tables, generates a searchable index.

## Project structure

```
├── build.py              # Static site generator (markdown → HTML)
├── template.html          # Shared shell with {{ placeholder }} markers
├── content/
│   ├── TEMPLATE.md        # Blank starter for new conditions
│   ├── radial-nerve-palsy.md
│   ├── ankle-sprain.md
│   └── ... (12 conditions and growing)
├── svg/
│   ├── radial-nerve-palsy.svg
│   └── ... (one SVG per condition)
├── scripts/
│   ├── create-batch.sh    # Kanban batch creation for AI workers
│   └── gen_flux.py        # FLUX medical illustration generator
└── dist/                  # Built site (gitignored, deployed via Actions)
```

## Content format

One markdown file per condition. YAML frontmatter + five sections:

```markdown
---
title: "Ankle Sprain"
aka: ["twisted ankle", "rolled ankle"]
category: musculoskeletal
body_region: lower-limb
icon: "🦶"
---

## ::gist::
### What is it?
Grade-6 explanation. Keep it under 120 words.

## ::adult::
### What's happening in your body
Grade-12 mechanism, symptoms, treatment.

## ::timeline::
- time: Day 1–3
  text: What happens.

## ::full::
### Pathophysiology
Current evidence, cited sources.

## ::sources::
- Real citations from PubMed, Cochrane, clinical guidelines.
```

## Batch production via AI workers

The project uses Hermes Kanban to batch-produce pages with AI workers. Each worker gets a task with condition-specific hints (key facts, red flags, treatment ladder) and the content template as reference. Workers research, write all three tiers, create the SVG, and self-verify by running `build.py`.

```bash
# Edit scripts/create-batch.sh with your conditions, then:
bash scripts/create-batch.sh
```

## Roadmap

- [ ] 12 conditions live, ~100 targeted
- [ ] JSON schema for declarative anatomy SVG generation
- [ ] Pagefind full-text search
- [ ] Category/body-region filter on index
- [ ] FLUX-powered medical illustration generator

## Deploy

GitHub Actions builds `dist/` and deploys to GitHub Pages. Every push to main redeploys.

## License

MIT
