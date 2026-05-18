#!/usr/bin/env python3
"""Scans all HTML files and generates a beautiful index.html."""

import os
import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent

SKIP = {"index.html", "design-system.html"}

FOLDER_LABELS = {
    "articles": "Articles",
    "specs":    "Specs",
    "reviews":  "Reviews",
    "reports":  "Reports",
    "explore":  "Explore",
    "tools":    "Tools",
}


def get_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<title>(.*?)</title>", text, re.IGNORECASE | re.DOTALL)
    return m.group(1).strip() if m else path.stem.replace("-", " ").title()


def get_description(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', text, re.IGNORECASE)
    return m.group(1).strip() if m else ""


def get_date(path: Path) -> str:
    m = re.match(r"(\d{4}-\d{2}-\d{2})", path.stem)
    return m.group(1) if m else ""


def collect_files():
    folders = {}
    for html in sorted(ROOT.rglob("*.html"), reverse=True):
        if html.name in SKIP:
            continue
        rel = html.relative_to(ROOT)
        parts = rel.parts
        folder = parts[0] if len(parts) > 1 else "."
        if folder.startswith("."):
            continue
        folders.setdefault(folder, []).append({
            "path": str(rel),
            "title": get_title(html),
            "description": get_description(html),
            "date": get_date(html),
        })
    return folders


def render_tab_buttons(folders):
    all_btn = '<button class="tab-btn active" onclick="filterFolder(\'all\', this)">All</button>'
    folder_btns = ""
    for folder in folders:
        label = FOLDER_LABELS.get(folder, folder.title())
        folder_btns += f'<button class="tab-btn" onclick="filterFolder(\'{folder}\', this)">{label}</button>'
    return all_btn + folder_btns


def render_cards(folders):
    html = ""
    for folder, files in folders.items():
        label = FOLDER_LABELS.get(folder, folder.title())
        for f in files:
            date_str = f"<span class='card-date'>{f['date']}</span>" if f["date"] else ""
            desc_str = f"<p class='card-desc'>{f['description']}</p>" if f["description"] else ""
            html += f"""
    <a class="card" href="{f['path']}" data-folder="{folder}">
      <div class="card-header">
        <span class="card-folder">{label}</span>
        {date_str}
      </div>
      <h3 class="card-title">{f['title']}</h3>
      {desc_str}
    </a>"""
    return html


def build(folders):
    tab_buttons = render_tab_buttons(folders)
    cards = render_cards(folders)
    total = sum(len(v) for v in folders.values())
    generated = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>My HTML Library</title>
<style>
:root {{
  --color-bg:#f5f2ed; --color-bg-alt:#eceae4; --color-bg-card:#ffffff;
  --color-text:#1a1a18; --color-text-muted:#6b6a63; --color-text-faint:#a09f97;
  --color-border:#dedad2; --color-accent:#d95f2b; --color-accent-hover:#c2521f;
  --color-accent-soft:#faeee7;
  --font-sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
  --text-sm:0.875rem; --text-base:1rem; --text-lg:1.125rem; --text-2xl:1.5rem; --text-3xl:1.875rem;
  --weight-medium:500; --weight-semibold:600; --weight-bold:700;
  --space-2:0.5rem; --space-3:0.75rem; --space-4:1rem; --space-6:1.5rem;
  --space-8:2rem; --space-12:3rem;
  --radius-md:8px; --radius-lg:12px;
  --shadow-sm:0 1px 3px rgba(0,0,0,0.07); --shadow-md:0 4px 12px rgba(0,0,0,0.08);
}}
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:var(--font-sans);background:var(--color-bg);color:var(--color-text);min-height:100vh}}
header{{background:var(--color-bg-card);border-bottom:1px solid var(--color-border);padding:var(--space-6) var(--space-8);display:flex;align-items:baseline;gap:var(--space-4);}}
header h1{{font-size:var(--text-2xl);font-weight:var(--weight-bold);}}
header .meta{{font-size:var(--text-sm);color:var(--color-text-faint);margin-left:auto}}
.container{{max-width:1100px;margin:0 auto;padding:var(--space-8)}}
.toolbar{{display:flex;align-items:center;gap:var(--space-2);flex-wrap:wrap;margin-bottom:var(--space-6)}}
.tab-btn{{
  padding:var(--space-2) var(--space-4);border:1px solid var(--color-border);
  background:var(--color-bg-card);color:var(--color-text-muted);
  border-radius:var(--radius-md);font-size:var(--text-sm);font-weight:var(--weight-medium);
  cursor:pointer;transition:all 120ms ease;
}}
.tab-btn:hover{{border-color:var(--color-accent);color:var(--color-accent)}}
.tab-btn.active{{background:var(--color-accent);border-color:var(--color-accent);color:#fff}}
.search{{margin-left:auto}}
.search input{{
  padding:var(--space-2) var(--space-4);border:1px solid var(--color-border);
  border-radius:var(--radius-md);font-size:var(--text-sm);background:var(--color-bg-card);
  color:var(--color-text);outline:none;width:200px;
}}
.search input:focus{{border-color:var(--color-accent)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:var(--space-4)}}
.card{{
  background:var(--color-bg-card);border:1px solid var(--color-border);border-radius:var(--radius-lg);
  padding:var(--space-6);text-decoration:none;color:inherit;display:block;
  box-shadow:var(--shadow-sm);transition:all 180ms ease;
}}
.card:hover{{box-shadow:var(--shadow-md);border-color:var(--color-accent);transform:translateY(-2px)}}
.card-header{{display:flex;align-items:center;justify-content:space-between;margin-bottom:var(--space-3)}}
.card-folder{{
  font-size:var(--text-sm);font-weight:var(--weight-medium);color:var(--color-accent);
  background:var(--color-accent-soft);padding:2px var(--space-2);border-radius:var(--radius-md);
}}
.card-date{{font-size:var(--text-sm);color:var(--color-text-faint)}}
.card-title{{font-size:var(--text-lg);font-weight:var(--weight-semibold);line-height:1.4;margin-bottom:var(--space-2)}}
.card-desc{{font-size:var(--text-sm);color:var(--color-text-muted);line-height:1.6}}
.empty{{text-align:center;color:var(--color-text-faint);padding:var(--space-12);font-size:var(--text-lg)}}
footer{{text-align:center;padding:var(--space-8);color:var(--color-text-faint);font-size:var(--text-sm);border-top:1px solid var(--color-border);margin-top:var(--space-12)}}
@media(max-width:600px){{
  header{{padding:var(--space-4)}}.container{{padding:var(--space-4)}}
  .search input{{width:100%}}.toolbar{{flex-direction:column;align-items:stretch}}
  .search{{margin-left:0}}
}}
</style>
</head>
<body>
<header>
  <h1>My HTML Library</h1>
  <span class="meta">{total} files · Updated {generated}</span>
</header>
<div class="container">
  <div class="toolbar">
    {tab_buttons}
    <div class="search"><input type="text" placeholder="Search..." oninput="filterSearch(this.value)"></div>
  </div>
  <div class="grid" id="grid">
    {cards}
  </div>
  <div class="empty" id="empty" style="display:none">No files found.</div>
</div>
<footer>Generated by GitHub Actions · <a href="design-system.html" style="color:var(--color-accent)">Design System</a></footer>
<script>
let currentFolder = 'all';
let currentSearch = '';
function update() {{
  const cards = document.querySelectorAll('.card');
  let visible = 0;
  cards.forEach(c => {{
    const folderMatch = currentFolder === 'all' || c.dataset.folder === currentFolder;
    const searchMatch = !currentSearch || c.textContent.toLowerCase().includes(currentSearch);
    const show = folderMatch && searchMatch;
    c.style.display = show ? '' : 'none';
    if (show) visible++;
  }});
  document.getElementById('empty').style.display = visible === 0 ? '' : 'none';
}}
function filterFolder(folder, btn) {{
  currentFolder = folder;
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  update();
}}
function filterSearch(val) {{
  currentSearch = val.toLowerCase();
  update();
}}
</script>
</body>
</html>
"""


if __name__ == "__main__":
    folders = collect_files()
    html = build(folders)
    out = ROOT / "index.html"
    out.write_text(html, encoding="utf-8")
    total = sum(len(v) for v in folders.values())
    print(f"Generated index.html — {total} files across {len(folders)} folders")
