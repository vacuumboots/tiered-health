#!/usr/bin/env python3
"""Build tiered-health pages from markdown content files.

Usage:
    python3 build.py                    # Build all conditions
    python3 build.py radial-nerve-palsy # Build one condition
    python3 build.py --list             # List available conditions
"""

import os, sys, re, glob, shutil, json
from pathlib import Path
from html import escape
from textwrap import dedent

ROOT = Path(__file__).resolve().parent
CONTENT_DIR = ROOT / "content"
SVG_DIR = ROOT / "svg"
DIST_DIR = ROOT / "dist"
TEMPLATE_PATH = ROOT / "template.html"

# ── Markdown → HTML converter ──────────────────────────────────────────

INLINE_TAGS = [
    (re.compile(r"\*\*\*(.+?)\*\*\*"), r"<strong><em>\1</em></strong>"),
    (re.compile(r"\*\*(.+?)\*\*"), r"<strong>\1</strong>"),
    (re.compile(r"\*(.+?)\*"), r"<em>\1</em>"),
    (re.compile(r"`([^`]+)`"), r"<code>\1</code>"),
    (re.compile(r"\[([^\]]+)\]\(([^)]+)\)"), r'<a href="\2">\1</a>'),
]


def apply_inline(text: str) -> str:
    for pattern, repl in INLINE_TAGS:
        text = pattern.sub(repl, text)
    return text


def markdown_to_html(md: str) -> str:
    """Convert a subset of markdown to HTML.

    Supports: h2/h3/h4, paragraphs, unordered/ordered lists,
    bold, italic, code, links, horizontal rules.
    Also supports ::callout:: and ::danger:: custom blocks.
    """
    lines = md.strip().split("\n")
    out = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Custom callout blocks
        m = re.match(r"^::danger::\s*$", line)
        if m:
            out.append('<div class="callout danger">')
            i += 1
            body_lines = []
            while i < len(lines) and not re.match(r"^::end::$", lines[i]):
                body_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1  # skip ::end::
            body = parse_block(body_lines)
            out.append(body)
            out.append("</div>")
            continue

        m = re.match(r"^::callout::\s*$", line)
        if m:
            out.append('<div class="callout">')
            i += 1
            body_lines = []
            while i < len(lines) and not re.match(r"^::end::$", lines[i]):
                body_lines.append(lines[i])
                i += 1
            if i < len(lines):
                i += 1
            body = parse_block(body_lines)
            out.append(body)
            out.append("</div>")
            continue

        # Heading
        m = re.match(r"^(#{1,4})\s+(.+)$", line)
        if m:
            level = len(m.group(1)) + 1  # h2→h2, h3→h3 in page context
            content = apply_inline(m.group(2))
            out.append(f"<h{level}>{content}</h{level}>")
            i += 1
            continue

        # Horizontal rule
        if re.match(r"^---+\s*$", line):
            out.append("<hr>")
            i += 1
            continue

        # Unordered list
        if re.match(r"^\s*-\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*-\s+", lines[i]):
                items.append(re.sub(r"^\s*-\s+", "", lines[i]))
                i += 1
            out.append("<ul>")
            for item in items:
                out.append(f"<li>{apply_inline(item)}</li>")
            out.append("</ul>")
            continue

        # Ordered list
        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", lines[i]))
                i += 1
            out.append("<ol>")
            for item in items:
                out.append(f"<li>{apply_inline(item)}</li>")
            out.append("</ol>")
            continue

        # Table: pipe-separated columns. Header row + separator row + data rows.
        table_match = re.match(r"^\|.+\|$", line)
        if table_match and i + 1 < len(lines) and re.match(r"^\|[\s\-:|]+\|$", lines[i + 1]):
            # Collect header
            headers = [c.strip() for c in line.split("|")[1:-1]]
            i += 2  # skip header and separator
            # Collect data rows
            rows = []
            while i < len(lines) and re.match(r"^\|.+\|$", lines[i]):
                cells = [c.strip() for c in lines[i].split("|")[1:-1]]
                rows.append(cells)
                i += 1
            out.append('<table class="data-table">')
            out.append("<thead><tr>")
            for h in headers:
                out.append(f"<th>{apply_inline(h)}</th>")
            out.append("</tr></thead>")
            out.append("<tbody>")
            for row in rows:
                out.append("<tr>")
                for cell in row:
                    out.append(f"<td>{apply_inline(cell)}</td>")
                out.append("</tr>")
            out.append("</tbody></table>")
            continue

        # Blank line → paragraph break
        if line.strip() == "":
            i += 1
            continue

        # Paragraph: collect consecutive non-special lines
        para_lines = []
        while i < len(lines) and lines[i].strip() != "" and not re.match(
            r"^(#{1,4}\s|::danger::|::callout::|::end::|^\s*-\s|^\s*\d+\.\s|---+|\|)",
            lines[i],
        ):
            para_lines.append(lines[i])
            i += 1
        if para_lines:
            out.append(f"<p>{apply_inline(' '.join(para_lines))}</p>")

    return "\n".join(out)


def parse_block(lines: list[str]) -> str:
    """Parse a block of lines (inside a callout) as markdown."""
    return markdown_to_html("\n".join(lines))


# ── Timeline parser ────────────────────────────────────────────────────

def parse_timeline(text: str) -> str:
    """Parse ::timeline:: section into HTML."""
    lines = text.strip().split("\n")
    items = []
    current_time = None
    current_text = []

    for line in lines:
        m = re.match(r"^-\s*time:\s*(.+)$", line)
        if m:
            if current_time:
                items.append((current_time, " ".join(current_text)))
            current_time = m.group(1).strip()
            current_text = []
        elif re.match(r"^\s+text:\s*(.+)$", line):
            current_text.append(re.match(r"^\s+text:\s*(.+)$", line).group(1).strip())
        elif line.strip() and current_time:
            current_text.append(line.strip())

    if current_time:
        items.append((current_time, " ".join(current_text)))

    if not items:
        return ""

    out = ['<div class="timeline">']
    for time, text in items:
        out.append('<div class="tl-item">')
        out.append(f'<div class="tl-time">{escape(time)}</div>')
        out.append(f'<div class="tl-text">{apply_inline(text)}</div>')
        out.append("</div>")
    out.append("</div>")
    return "\n".join(out)


# ── Frontmatter parser ─────────────────────────────────────────────────

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Parse YAML-like frontmatter from markdown. Returns (meta, body)."""
    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    meta = {}
    for line in parts[1].strip().split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r"^(\w[\w_-]*):\s*(.+)$", line)
        if m:
            key = m.group(1)
            val = m.group(2).strip()

            # List values: [a, b, c]
            if val.startswith("[") and val.endswith("]"):
                items = re.findall(r'"([^"]*)"', val)
                if not items:
                    items = [x.strip() for x in val[1:-1].split(",") if x.strip()]
                meta[key] = items
            # Unquoted string
            elif val.startswith('"') and val.endswith('"'):
                meta[key] = val[1:-1]
            else:
                meta[key] = val

    return meta, parts[2]


# ── Section parser ─────────────────────────────────────────────────────

def parse_sections(body: str) -> dict:
    """Split body into ::section:: blocks. Returns {name: content}."""
    sections = {}
    current_section = None
    current_content = []

    for line in body.split("\n"):
        m = re.match(r"^##\s+::(\w+)::$", line)
        if m:
            if current_section:
                sections[current_section] = "\n".join(current_content)
            current_section = m.group(1)
            current_content = []
        elif current_section:
            current_content.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_content)

    return sections


# ── Build one page ─────────────────────────────────────────────────────

def build_page(slug: str) -> bool:
    """Build a single condition page. Returns True on success."""
    md_path = CONTENT_DIR / f"{slug}.md"
    svg_path = SVG_DIR / f"{slug}.svg"

    if not md_path.exists():
        print(f"  ✗ Content file not found: {md_path}")
        return False

    # Read template
    template = TEMPLATE_PATH.read_text()

    # Parse content
    raw = md_path.read_text()
    meta, body = parse_frontmatter(raw)
    sections = parse_sections(body)

    # Convert sections
    gist_html = markdown_to_html(sections.get("gist", ""))
    adult_html = markdown_to_html(sections.get("adult", ""))
    full_html = markdown_to_html(sections.get("full", ""))
    timeline_html = parse_timeline(sections.get("timeline", ""))
    sources_html = markdown_to_html(sections.get("sources", ""))

    # AKA line
    aka = meta.get("aka", [])
    if isinstance(aka, str):
        aka = [aka]
    aka_html = ""
    if aka:
        aka_html = f'<p class="aka">Also called: {" · ".join(escape(a) for a in aka)}</p>'

    # Anatomy SVG
    svg_content = ""
    if svg_path.exists():
        svg_raw = svg_path.read_text()
        # Extract just the <svg>...</svg> part
        svg_match = re.search(r"<svg[\s\S]*?</svg>", svg_raw, re.IGNORECASE)
        if svg_match:
            svg_content = svg_match.group(0)
        else:
            svg_content = svg_raw
    # If no SVG file, check for inline ::svg:: section (unusual but supported)
    if not svg_content and "svg" in sections:
        svg_content = sections["svg"].strip()

    anatomy_html = ""
    if svg_content:
        anatomy_html = f"""  <div class="anatomy-box">
    <h3>Anatomy</h3>
    {svg_content}
  </div>"""

    # Timeline section
    timeline_section = ""
    if timeline_html:
        timeline_section = f"""
    <h3>Recovery Timeline</h3>
    {timeline_html}"""

    # Sources section
    sources_section = ""
    if sources_html.strip():
        sources_section = f"""
    <h3>Key Sources</h3>
    {sources_html}"""

    # Build replacements
    title = meta.get("title", slug.replace("-", " ").title())
    icon = meta.get("icon", "")
    category = meta.get("category", "")
    body_region = meta.get("body_region", "")
    last_reviewed = meta.get("last_reviewed", "Unreviewed")

    # Inject timeline into adult tier
    adult_with_timeline = adult_html + timeline_section

    # Inject sources into full tier
    full_with_sources = full_html + sources_section

    replacements = {
        "{{ TITLE }}": escape(title),
        "{{ ICON }}": icon,
        "{{ AKA_HTML }}": aka_html,
        "{{ CATEGORY }}": escape(category),
        "{{ BODY_REGION }}": escape(body_region),
        "{{ ANATOMY_SECTION }}": anatomy_html,
        "{{ TIER_GIST }}": gist_html,
        "{{ TIER_ADULT }}": adult_with_timeline,
        "{{ TIER_FULL }}": full_with_sources,
        "{{ LAST_REVIEWED }}": escape(last_reviewed),
    }

    html = template
    for key, val in replacements.items():
        html = html.replace(key, val)

    # Write output
    DIST_DIR.mkdir(exist_ok=True)
    out_path = DIST_DIR / f"{slug}.html"
    out_path.write_text(html)

    return True


# ── Main ────────────────────────────────────────────────────────────────

def get_all_conditions() -> list[dict]:
    """Read all content files and return metadata for index."""
    conditions = []
    for md_path in sorted(CONTENT_DIR.glob("*.md")):
        if md_path.stem == "TEMPLATE":
            continue
        raw = md_path.read_text()
        meta, body = parse_frontmatter(raw)
        sections = parse_sections(body)
        # Get first paragraph of gist as preview
        gist = sections.get("gist", "").strip()
        preview = ""
        for line in gist.split("\n"):
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("::"):
                preview = line[:160]
                break
        conditions.append({
            "slug": md_path.stem,
            "title": meta.get("title", md_path.stem.replace("-", " ").title()),
            "aka": meta.get("aka", []),
            "category": meta.get("category", ""),
            "body_region": meta.get("body_region", ""),
            "icon": meta.get("icon", ""),
            "preview": preview,
        })
    return conditions


def build_index():
    """Generate dist/index.html listing all conditions with search."""
    conditions = get_all_conditions()
    if not conditions:
        return

    cards_html = []
    for c in conditions:
        aka_str = ""
        aka = c["aka"]
        if isinstance(aka, str):
            aka = [aka]
        if aka:
            aka_str = " · ".join(escape(a) for a in aka)
        cards_html.append(f"""    <a href="{c['slug']}.html" class="card" data-search="{escape(c['title']).lower()} {aka_str.lower()} {escape(c['category']).lower()}">
      <div class="card-icon">{c['icon']}</div>
      <div class="card-body">
        <h3>{escape(c['title'])}</h3>
        {f'<p class="card-aka">{aka_str}</p>' if aka_str else ''}
        <p class="card-preview">{escape(c['preview'])}</p>
      </div>
    </a>""")

    conditions_json = json.dumps([
        {"slug": c["slug"], "title": c["title"], "aka": c["aka"] if isinstance(c["aka"], list) else [c["aka"]] if c["aka"] else [],
         "category": c["category"], "body_region": c["body_region"], "icon": c["icon"]}
        for c in conditions
    ])

    index_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tiered Health — Common Injuries &amp; Ailments</title>
<meta name="description" content="One page per injury/ailment with three reading levels: Gist (grade 6), Adult (grade 12), and Full (best current evidence).">
<style>
  :root {{
    --bg: #fafaf8; --surface: #ffffff; --text: #1a1a1a; --text-muted: #5c5c5c;
    --accent: #2d6a6e; --accent-light: #e8f3f3; --border: #e0e0dc;
    --radius: 8px; --shadow: 0 1px 3px rgba(0,0,0,0.06);
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{ --bg: #1a1a1a; --surface: #242424; --text: #e8e8e4;
      --text-muted: #a0a0a0; --accent: #5cbcbf; --accent-light: #1e3030;
      --border: #383838; }}
  }}
  *,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
  html{{font-size:17px}}
  body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:var(--bg);color:var(--text);line-height:1.6;-webkit-font-smoothing:antialiased}}
  header{{background:var(--surface);border-bottom:1px solid var(--border);padding:1.5rem 1.25rem;text-align:center;box-shadow:var(--shadow)}}
  header h1{{font-size:1.5rem;color:var(--accent)}}
  header p{{color:var(--text-muted);margin-top:0.3rem;font-size:0.9rem}}
  .search-wrap{{max-width:600px;margin:1rem auto 0}}
  .search-wrap input{{width:100%;padding:0.6rem 1rem;border:1px solid var(--border);border-radius:24px;font-size:0.95rem;background:var(--bg);color:var(--text);outline:none}}
  .search-wrap input:focus{{border-color:var(--accent)}}
  main{{max-width:900px;margin:0 auto;padding:2rem 1.25rem 4rem}}
  .grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:1rem}}
  .card{{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem;text-decoration:none;color:var(--text);transition:box-shadow 0.15s;display:flex;gap:0.75rem;align-items:flex-start}}
  .card:hover{{box-shadow:0 4px 12px rgba(0,0,0,0.08)}}
  .card-icon{{font-size:1.8rem;flex-shrink:0;width:2.5rem;text-align:center}}
  .card-body h3{{font-size:1rem;color:var(--accent);margin-bottom:0.2rem}}
  .card-aka{{font-size:0.75rem;color:var(--text-muted);margin-bottom:0.3rem}}
  .card-preview{{font-size:0.82rem;color:var(--text-muted);line-height:1.45}}
  .empty{{text-align:center;color:var(--text-muted);padding:2rem;display:none}}
  .count{{font-size:0.8rem;color:var(--text-muted);margin-bottom:1rem}}
  footer{{text-align:center;padding:2rem;color:var(--text-muted);font-size:0.8rem;border-top:1px solid var(--border)}}
</style>
</head>
<body>
<header>
  <h1>🩺 Tiered Health</h1>
  <p>One page per injury or ailment — three reading levels, visual anatomy, current evidence.</p>
  <div class="search-wrap"><input type="search" id="search" placeholder="Search conditions…" autofocus></div>
</header>
<main>
  <p class="count" id="count">{len(conditions)} condition{'' if len(conditions)==1 else 's'}</p>
  <div class="grid" id="grid">
{chr(10).join(cards_html)}
  </div>
  <p class="empty" id="empty">No conditions match your search.</p>
</main>
<footer>
  <p>Last built: {__import__('datetime').datetime.now().strftime('%B %d, %Y')}</p>
  <p><strong>Disclaimer:</strong> Educational purposes only. Not medical advice.</p>
</footer>
<script>
const DATA = {conditions_json};
const grid = document.getElementById('grid');
const empty = document.getElementById('empty');
const count = document.getElementById('count');
const cards = grid.querySelectorAll('.card');
document.getElementById('search').addEventListener('input', function() {{
  const q = this.value.toLowerCase().trim();
  let visible = 0;
  cards.forEach(c => {{
    const match = !q || c.dataset.search.includes(q);
    c.style.display = match ? '' : 'none';
    if (match) visible++;
  }});
  count.textContent = (q ? visible + ' of ' : '') + '{len(conditions)} condition{'' if len(conditions)==1 else 's'}';
  empty.style.display = visible ? 'none' : 'block';
}});
</script>
</body>
</html>"""

    (DIST_DIR / "index.html").write_text(index_html)

def main():
    if not TEMPLATE_PATH.exists():
        print("✗ template.html not found. Run from tiered-health directory.")
        sys.exit(1)

    CONTENT_DIR.mkdir(exist_ok=True)
    SVG_DIR.mkdir(exist_ok=True)

    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg == "--list":
            slugs = sorted(
                [p.stem for p in CONTENT_DIR.glob("*.md") if p.stem != "TEMPLATE"]
            )
            if slugs:
                print("Available conditions:")
                for s in slugs:
                    print(f"  {s}")
            else:
                print("No content files found in content/")
            return

        # Build one
        slug = arg.replace(".md", "")
        print(f"Building: {slug}")
        if build_page(slug):
            print(f"  → dist/{slug}.html")
            build_index()
            print(f"  → dist/index.html")
        else:
            sys.exit(1)
    else:
        # Build all
        slugs = sorted(
            [p.stem for p in CONTENT_DIR.glob("*.md") if p.stem != "TEMPLATE"]
        )
        if not slugs:
            print("No content files found in content/")
            return

        print(f"Building {len(slugs)} condition(s)...")
        ok = 0
        for slug in slugs:
            if build_page(slug):
                print(f"  ✓ {slug}")
                ok += 1
            else:
                print(f"  ✗ {slug}")
        build_index()
        print(f"  ✓ index.html ({len(slugs)} conditions)")
        print(f"\nDone: {ok}/{len(slugs)} built → dist/")


if __name__ == "__main__":
    main()
