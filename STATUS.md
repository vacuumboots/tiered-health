# Tiered Health — Status

## What we've built

### The site
**22 conditions live** at `vacuumboots.github.io/tiered-health`. Every page has three reading levels (Gist grade 6 / Adult grade 12 / Full evidence), an SVG anatomy diagram, a visual recovery timeline, and a diagnostic workup table. Dark mode is automatic via `prefers-color-scheme`. Print mode shows all three tiers. Accessibility: skip-to-content link, focus-visible outlines, back-to-index navigation.

| Category | Conditions |
|----------|-----------|
| Musculoskeletal | Ankle sprain, sciatica, herniated disc, gout, plantar fasciitis, tendonitis, bursitis, frozen shoulder |
| Neurological | Migraine, carpal tunnel syndrome, radial nerve palsy |
| Respiratory | Sinusitis, pneumonia, influenza, acute bronchitis |
| Gastrointestinal | GERD, peptic ulcer disease, IBS, gallstones, pancreatitis |
| Urological | Kidney stones, UTI |

### The pipeline
- **`build.py`** — zero-dependency static site generator (Python stdlib only). Parses YAML frontmatter + markdown sections, converts to HTML with table/callout/timeline support, inlines SVGs, generates searchable index page. Outputs to `docs/` for GitHub Pages.
- **`template.html`** — shared shell with `{{ PLACEHOLDER }}` markers. All CSS, JS tier toggle, dark mode, print styles live here once.
- **Content format** — `## ::gist::` / `::adult::` / `::full::` / `::timeline::` / `::sources::` delimited sections in a single markdown file. `content/TEMPLATE.md` as starter.
- **SVG anatomy diagrams** — one per condition at `svg/{slug}.svg`. Clean medical illustration style.

### The kanban workflow
- **Two batches produced**: 20 conditions written by AI workers (Hermes Kanban + writer profile)
- **`scripts/create-batch.sh`** — reusable batch creation script. Each task gets condition-specific hints (key facts, red flags, treatment ladder, differentials) so workers don't waste turns researching basics
- **Worker self-verification**: each worker runs `build.py {slug}` before completing, catches rendering issues
- **Average completion time**: ~4 minutes per condition

### GitHub & deployment
- **Repo**: `github.com/vacuumboots/tiered-health` (public, MIT license)
- **Deployed**: GitHub Pages from `main` branch, `/docs` folder
- **Actions workflow** written (`.github/workflows/deploy.yml`) but blocked on OAuth `workflow` scope — needs `gh auth refresh -h github.com -s workflow` to activate

### Documentation
- `README.md` — project overview, quick start, structure, format reference
- `TODO.md` — prioritized task list
- `LOG.md` — session history
- `USER_steps.md` — 10 step-by-step guides for human-in-the-loop actions
- `Top-Human-Medical-Ailments.md` — 300-condition reference list (gitignored, personal)

### Skills
- **`tiered-health-pipeline`** saved to `~/.hermes/skills/software-development/` — full end-to-end workflow, content schema, build pipeline usage, kanban batch deployment pattern. Includes `scripts/create-batch.sh` and `references/content-template.md`.
- **Concept page** at `~/wiki/concepts/tiered-health-pages.md` — original design doc with architecture decisions, pitfalls, expansion path

---

## What's left

### Content — Batch 3 (~10 conditions)
From `Top-Human-Medical-Ailments.md`:
- Bell's Palsy, Tension Headaches, Shingles, Appendicitis, Hemorrhoids
- Laryngitis, Contact Dermatitis, Acne, Eczema, Psoriasis

### Content — Batch 4+ (ongoing)
Target: 100 conditions. The reference list has 300. Priority order:
1. Acute/common conditions people search "what to do for X" (batches 1-3 cover most)
2. Remaining musculoskeletal, neurological, respiratory
3. Mental health (needs different treatment approach — less "what to do right now," more "when to seek help")
4. Chronic diseases, cancers (different format consideration — these aren't self-limiting injuries)

### Illustration
**Current state**: AI-written SVGs. Quality is variable — some are clean anatomical diagrams, others are rough approximations. No medical review has been applied.
**Options explored**:
- FLUX.1 Dev local (MLX/Diffusers): failed — 23GB download impossible on current connection, 46+ hours estimated
- Replicate API: not tested (user had auth issues)
- ComfyUI: available via skill, requires local GPU setup
- JSON schema approach (declarative): not started — most promising for accuracy
**Decision**: No illustrations for now. Revisit when internet connection improves or a working API key is available.

### Pipeline improvements
- [ ] **Pagefind full-text search** — current index search only matches title/aka. Pagefind would index all three tiers, making the site genuinely searchable by symptom or treatment
- [ ] **Category/body-region filter** on index page — filter cards by category or body region
- [ ] **Dark mode toggle** — manual override for system preference
- [ ] **Next/previous condition** navigation at bottom of each page
- [ ] **Favicon**
- [ ] **`build.py --watch`** mode — filesystem watcher for live rebuild during editing

### Deployment
- [ ] **Activate GitHub Actions** — run `gh auth refresh -h github.com -s workflow && git push`. After this, every push auto-builds and deploys
- [ ] **Custom domain** — medical content should live on its own domain, not a personal GitHub Pages subdomain. Suggested: `tieredhealth.org` or similar
- [ ] **SSL/HTTPS** — automatic with Cloudflare Pages or Netlify (free)

### Quality
- [ ] **Medical accuracy review** — none of the 20 AI-written pages have been reviewed by a human. The Full tier cites real sources (Cochrane, PubMed, clinical guidelines) but citations may be inaccurate or fabricated by the LLM. Spot-check needed before trusting.
- [ ] **Gist tier readability audit** — are the grade-6 summaries actually grade-6? Run through a readability scorer (Flesch-Kincaid)
- [ ] **Cross-reference against NIH MedlinePlus** — compare 5 random pages against the gold standard for consumer health information

### Long-term
- [ ] **Translations** — Gist tier in top 10 languages (Spanish, Mandarin, Hindi, Arabic, etc.)
- [ ] **Symptom checker** — lightweight triage tool (NOT a diagnosis tool — legal minefield, needs lawyer review)
- [ ] **Interactive body map** — click a body part → see relevant conditions
- [ ] **Video** — short animated explainers per condition, same three-tier structure
- [ ] **Print-friendly PDF export** — single-page PDF per condition for clinic handouts
- [ ] **Accessibility audit** — WCAG 2.1 AA compliance check
