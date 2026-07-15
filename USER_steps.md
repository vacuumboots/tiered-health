# USER_steps.md — Human-in-the-Loop Actions

When the agent hits a wall and a human needs to step in, read the relevant section below.

## Deployment

### 1. Register a domain
- Pick a domain registrar (Cloudflare, Namecheap, Porkbun)
- Buy a domain — medical health content should NOT be a subdomain of a personal site
- Suggested: something like `tieredhealth.org` or similar

### 2. Deploy to Cloudflare Pages
1. Push the repo to GitHub
2. Go to Cloudflare Dashboard → Workers & Pages → Create → Pages
3. Connect GitHub repo
4. Build settings:
   - Build command: `python3 build.py`
   - Output directory: `dist`
5. Deploy
6. Add custom domain in Cloudflare Pages → Custom domains

### 3. Alternative: Deploy to Netlify
1. Push repo to GitHub
2. Netlify → Add new site → Import from Git
3. Build command: `python3 build.py`
4. Publish directory: `dist`

## Content Review

### 4. Spot-check a page for medical accuracy
1. Open `dist/condition-name.html` in browser
2. Switch to Full tier
3. Verify: do the cited sources actually exist? (Spot-check 2-3 references on PubMed)
4. Verify: are red flags correct? (Compare with UpToDate or NIH MedlinePlus)
5. Verify: is the Gist tier truly grade-6 readable? (Read it aloud — does it feel natural?)

### 5. Fix an inaccurate SVG
1. Open `svg/condition-name.svg` in a vector editor (Figma, Inkscape, Illustrator)
2. Fix the anatomy
3. Run `python3 build.py condition-name` to rebuild
4. Verify the fix in `dist/condition-name.html`

## Kanban

### 6. Create the next batch of conditions
1. Edit `create-batch.sh`
2. Replace the `create_task` calls with new conditions
3. Each needs: slug, title, icon, category, body_region, aka, hints
4. Run: `cd ~/Git/tiered-health && bash create-batch.sh`

### 7. Check worker output
1. `hermes kanban dashboard` — interactive board view
2. `hermes kanban show <task-id>` — see completion summary
3. Bad output? Archive the task and re-create with better hints

### 8. Unstick a stuck worker
1. `hermes kanban list` — find stuck task
2. `hermes kanban reclaim <id>` — release the claim
3. If work was partially done, check files and either:
   - `hermes kanban complete <id> --summary "..."` (if work is good)
   - `hermes kanban unblock <id>` to retry

## Maintenance

### 9. Rebuild the site after template changes
1. Make changes to `template.html` or `build.py`
2. Run `python3 build.py` (rebuilds all pages + index)
3. Spot-check a few pages in dark + light mode

### 10. Add a new CSS fix or feature
1. Edit `template.html` (CSS in `<style>`, HTML structure, JS)
2. Run `python3 build.py`
3. `open dist/index.html` — verify
4. Commit both `template.html` and `dist/`
