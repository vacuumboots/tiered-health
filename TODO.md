# Tiered Health — TODO

## Now
- [ ] CSS: fix white-on-white danger callout in dark mode ✓ (done)
- [ ] UX: add skip-to-content link, back-to-index ✓ (done)
- [ ] Audit all 12 pages for quality (spot-check rendered output)
- [ ] Fix any raw markdown leaks or broken SVGs

## Next
- [ ] UX: add category/body-region filter to index page
- [ ] UX: add "next condition" link at bottom of each page
- [ ] UX: dark mode toggle (override system preference)
- [ ] Fix content/TEMPLATE.md formatting (ensure it renders clean as a demo)
- [ ] Add favicon

## Content — Batch 2 (prioritize from Top-Human-Medical-Ailments.md)
- [ ] Pneumonia
- [ ] Influenza
- [ ] Acute Bronchitis
- [ ] Peptic Ulcer Disease
- [ ] IBS
- [ ] Gallstones
- [ ] Pancreatitis
- [ ] Tendonitis
- [ ] Bursitis
- [ ] Frozen Shoulder

## Content — Batch 3
- [ ] Bell's Palsy
- [ ] Tension Headaches
- [ ] Shingles
- [ ] Appendicitis
- [ ] Hemorrhoids
- [ ] Laryngitis
- [ ] Contact Dermatitis
- [ ] Acne
- [ ] Eczema
- [ ] Psoriasis

## Image Generation
- [ ] Research JSON schema approach for anatomy SVGs (declarative, not generative)
- [ ] Test ComfyUI integration for medical illustration (see comfyui skill)
- [ ] Evaluate SVG quality across all 12 workers — flag inaccurate ones

## Pipeline
- [ ] RSS/Atom feed for new conditions
- [ ] Add `build.py --watch` mode (filesystem watcher)
- [ ] Pagefind search (full-text, not just title/aka match)
- [ ] Automated medical review check (LLM reads Full tier, flags dubious claims)

## Deployment
- [ ] Choose domain
- [ ] Deploy static site (Cloudflare Pages or Netlify)
- [ ] Set up CI: push to main → build → deploy
