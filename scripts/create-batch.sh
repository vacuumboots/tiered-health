#!/bin/bash
# Batch-create tiered-health kanban tasks
# Run: bash create-batch.sh

BOARD="tiered-health"
WORKSPACE="dir:/Users/administrator/Git/tiered-health"

switch() {
  hermes kanban boards switch "$BOARD" > /dev/null 2>&1
}

create_task() {
  local slug="$1"
  local title="$2"
  local icon="$3"
  local category="$4"
  local body_region="$5"
  local aka="$6"
  local hints="$7"

  switch
  hermes kanban create "Write content/${slug}.md + svg/${slug}.svg" \
    --assignee writer \
    --workspace "$WORKSPACE" \
    --body "## Project: Tiered Health

Write content/${slug}.md and svg/${slug}.svg for **${title}**.

## Reference files
- Read content/TEMPLATE.md for the exact format
- Read content/radial-nerve-palsy.md and content/ankle-sprain.md for quality reference
- SVG style: match svg/radial-nerve-palsy.svg and svg/ankle-sprain.svg

## Frontmatter
- title: \"${title}\"
- aka: [${aka}]
- category: ${category}
- body_region: ${body_region}
- last_reviewed: \"July 2026\"
- icon: \"${icon}\"

## Condition-specific hints
${hints}

## Tier requirements
- **Gist** (grade 6, ~80-120 words): one sentence what it is, 3-5 bullet what to do, ::danger:: for ER signs, ::callout:: for reassurance
- **Adult** (grade 12, ~400-600 words): mechanism, symptoms, recovery timeline, treatment options, what NOT to do
- **Full** (best evidence): pathophysiology, differential diagnosis, diagnostic workup as pipe table, evidence summary with real citations, surgical options if applicable, open questions

## SVG
Create svg/${slug}.svg — anatomy/mechanism diagram with clear labels. ViewBox ~500x500. Style: clean medical illustration, thin lines, muted colors.

## Research
Search PubMed, Cochrane, clinical guidelines. Cite real sources in ::sources::. Do not fabricate references.

## Verify
After writing: python3 build.py ${slug} — check all tiers render, table works, SVG displays, no raw markdown leaks." \
    --json 2>&1 | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'  {d[\"id\"][:12]}  {d[\"title\"][:55]}')"
}

echo "Creating batch 1 on board: $BOARD"
echo ""

create_task "migraine" "Migraine" "🧠" "neurological" "head-neck" \
  "\"migraine headache\"" \
  "- Classic phases: prodrome, aura, headache, postdrome. Triggers: stress, food, hormones, sleep, weather.
- Common abortives: triptans, gepants, NSAIDs. Preventives: beta-blockers, CGRP antibodies, Botox.
- Red flags: thunderclap onset, first after 50, systemic symptoms, focal neuro deficits that don't resolve."

create_task "carpal-tunnel-syndrome" "Carpal Tunnel Syndrome" "🖐️" "neurological" "upper-limb" \
  "\"CTS, median nerve compression\"" \
  "- Median nerve compression at the wrist. Phalen's and Tinel's signs. Thenar atrophy in late stages.
- Nighttime symptoms are classic. Splinting at night is first-line.
- Differential: C6 radiculopathy, pronator teres syndrome, peripheral neuropathy."

create_task "sciatica" "Sciatica" "🦵" "musculoskeletal" "lower-limb" \
  "\"lumbar radiculopathy, pinched nerve\"" \
  "- Usually from L4-L5 or L5-S1 disc herniation compressing the sciatic nerve. Pain radiating from low back down leg.
- Red flags: saddle anesthesia, bowel/bladder dysfunction (cauda equina — surgical emergency).
- Most resolve conservatively in 6-8 weeks. PT, NSAIDs, epidural steroids if severe."

create_task "herniated-disc" "Herniated Disc" "🦴" "musculoskeletal" "torso" \
  "\"slipped disc, disc herniation, ruptured disc\"" \
  "- Most common at L4-L5 and L5-S1. Disc material protrudes through annular tear, compressing nerve root.
- MRI is gold standard for diagnosis. Most improve without surgery.
- Surgical options: microdiscectomy, laminectomy. Indications: progressive neuro deficit, cauda equina, refractory pain >6 weeks."

create_task "gout" "Gout" "🦶" "musculoskeletal" "lower-limb" \
  "\"gouty arthritis, podagra\"" \
  "- Inflammatory arthritis from monosodium urate crystal deposition. Classic: acute first MTP joint (podagra).
- Diagnosed by joint aspiration showing negatively birefringent crystals under polarized light.
- Acute treatment: NSAIDs, colchicine, corticosteroids. Urate-lowering: allopurinol, febuxostat.
- Dietary: limit purines (red meat, shellfish, beer), hydrate well."

create_task "kidney-stones" "Kidney Stones" "🪨" "urological" "torso" \
  "\"nephrolithiasis, renal calculi\"" \
  "- Calcium oxalate most common (80%). Present with severe flank pain radiating to groin, hematuria.
- CT non-contrast is gold standard. <5mm usually pass spontaneously with hydration and NSAIDs.
- Prevention: high fluid intake, low sodium, low oxalate diet. Tamsulosin for medical expulsive therapy.
- Surgical: ESWL, ureteroscopy with laser lithotripsy, PCNL for large stones."

create_task "urinary-tract-infection" "Urinary Tract Infection" "🚽" "urological" "torso" \
  "\"UTI, bladder infection, cystitis\"" \
  "- E. coli causes 80%+ of uncomplicated UTIs. Classic: dysuria, frequency, urgency, suprapubic pain.
- Dipstick: leukocyte esterase + nitrites. Culture is gold standard.
- Uncomplicated: nitrofurantoin or TMP-SMX x3-5 days. Complicated: fluoroquinolones, broader spectrum.
- Pyelonephritis = upper tract (fever, flank pain) — more serious, often needs IV antibiotics."

create_task "plantar-fasciitis" "Plantar Fasciitis" "👣" "musculoskeletal" "lower-limb" \
  "\"heel pain, plantar fasciopathy\"" \
  "- Degenerative (not inflammatory) change in plantar fascia. Classic: first-step pain in the morning.
  - Risk factors: obesity, prolonged standing, flat feet, tight Achilles.
  - Treatment: stretching (Achilles + plantar fascia), night splints, supportive shoes, NSAIDs.
  - Refractory: shockwave therapy, corticosteroid injection, platelet-rich plasma. Surgery is last resort."

create_task "sinusitis" "Sinusitis" "👃" "respiratory" "head-neck" \
  "\"sinus infection, rhinosinusitis\"" \
  "- Viral most common (<10 days). Bacterial if symptoms >10 days or double-sickening pattern.
  - Key symptoms: facial pressure/pain, nasal congestion, purulent discharge, headache, tooth pain.
  - Treatment: saline irrigation, decongestants (max 3 days), intranasal corticosteroids. Antibiotics only if bacterial.
  - Red flags: periorbital swelling, visual changes, severe headache — think orbital cellulitis or intracranial extension."

create_task "gerd" "GERD" "🔥" "gastrointestinal" "torso" \
  "\"acid reflux, heartburn, gastroesophageal reflux disease\"" \
  "- Lower esophageal sphincter dysfunction allows gastric acid into esophagus. Classic: burning retrosternal pain after meals, worse lying down.
  - Alarm symptoms: dysphagia, odynophagia, weight loss, anemia, early satiety — need endoscopy to rule out malignancy/Barrett's.
  - Treatment ladder: lifestyle (elevate HOB, avoid triggers) → antacids → H2 blockers → PPIs.
  - Long-term PPI risks: B12 deficiency, C. diff, kidney disease, osteoporosis. Fundoplication for refractory cases."

echo ""
echo "Done. Run 'hermes kanban boards' to check."