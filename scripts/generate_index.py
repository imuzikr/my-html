#!/usr/bin/env python3
"""Generates main index (category cards) and per-category sub-indexes."""

import re
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).parent.parent

SKIP = {"index.html", "design-system.html"}

CATEGORY_META = {
    "insights": {
        "label": "Insights",
        "description": "연구 · 분석 · 학술 콘텐츠",
        "grad_from": "2d5a8e",
        "grad_to": "1e3d6b",
        "gradients": [("2d5a8e","1e3d6b"), ("234e80","163460"), ("3666a0","244e82"), ("1e3d6b","122845")],
    },
    "vibe": {
        "label": "Vibe",
        "description": "웹 개발 · 네트워크 · 바이브 코딩",
        "grad_from": "d95f2b",
        "grad_to": "b84820",
        "gradients": [("d95f2b","b84820"), ("bf4e20","9e3c16"), ("e07035","c85428"), ("b85020","9a3e16")],
    },
}

KNOWN_CATEGORIES = list(CATEGORY_META.keys())


# ── File metadata helpers ────────────────────────────────────────────────────

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


def get_og_image(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r'<meta\s+property=["\']og:image["\']\s+content=["\'](.*?)["\']', text, re.IGNORECASE)
    if not m:
        m = re.search(r'<meta\s+content=["\'](.*?)["\']\s+property=["\']og:image["\']', text, re.IGNORECASE)
    return m.group(1).strip() if m else ""


def collect_files():
    """Collect files from known category folders only."""
    folders = {}
    for category in KNOWN_CATEGORIES:
        folder_path = ROOT / category
        if not folder_path.exists():
            continue
        files = []
        for html in sorted(folder_path.glob("*.html"), reverse=True):
            if html.name in SKIP:
                continue
            files.append({
                "name": html.name,
                "path": f"{category}/{html.name}",
                "title": get_title(html),
                "description": get_description(html),
                "date": get_date(html),
                "og_image": get_og_image(html),
            })
        if files:
            folders[category] = files
    return folders


# ── Back-to-index button ─────────────────────────────────────────────────────

BACK_BUTTON_MARKER = 'id="back-to-index"'


def _back_button_snippet(href: str) -> str:
    return (
        '\n<!-- Back to index -->\n'
        f'<a id="back-to-index" href="{href}"'
        ' aria-label="목록으로 돌아가기" title="목록으로">'
        '<svg viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg"'
        ' width="18" height="18">'
        '<path d="M8.5 15L3 10l5.5-5" stroke="white" stroke-width="2"'
        ' stroke-linecap="round" stroke-linejoin="round"/>'
        '<path d="M3 10h14" stroke="white" stroke-width="2" stroke-linecap="round"/>'
        '</svg></a>\n'
        '<style>\n'
        '#back-to-index{position:fixed;bottom:1.5rem;left:1.5rem;width:44px;height:44px;'
        'background:#6b6a63;color:#fff;border-radius:9999px;display:flex;'
        'align-items:center;justify-content:center;text-decoration:none;'
        'box-shadow:0 4px 16px rgba(0,0,0,.18);transition:background .15s,transform .15s;z-index:800;}\n'
        '#back-to-index:hover{background:#d95f2b;transform:translateX(-2px);}\n'
        '@media(max-width:600px){#back-to-index{bottom:1rem;left:1rem;}}\n'
        '</style>\n'
    )


def inject_back_button(path: Path) -> bool:
    """Inject back button pointing to same-folder index.html (the sub-index)."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    if BACK_BUTTON_MARKER in text:
        return False
    if "</body>" not in text:
        return False
    snippet = _back_button_snippet("index.html")
    path.write_text(text.replace("</body>", snippet + "</body>", 1), encoding="utf-8")
    return True


# ── Mobile font scaling injection ───────────────────────────────────────────

MOBILE_FONT_MARKER = 'id="mobile-font-scale"'

MOBILE_FONT_CSS = (
    '\n<style id="mobile-font-scale">\n'
    '@media(max-width:700px){\n'
    '  :root{\n'
    '    --text-sm:1rem;\n'
    '    --text-base:1.15rem;\n'
    '    --text-lg:1.35rem;\n'
    '    --text-xl:1.55rem;\n'
    '    --text-2xl:1.85rem;\n'
    '    --text-3xl:2.25rem;\n'
    '  }\n'
    '}\n'
    '</style>\n'
)


def inject_mobile_fonts(path: Path) -> bool:
    """Inject mobile font scaling into article files that don't have it yet."""
    text = path.read_text(encoding="utf-8", errors="ignore")
    if MOBILE_FONT_MARKER in text:
        return False
    if "</head>" not in text:
        return False
    path.write_text(text.replace("</head>", MOBILE_FONT_CSS + "</head>", 1), encoding="utf-8")
    return True


# ── Shared CSS ───────────────────────────────────────────────────────────────

SHARED_CSS = """
:root {
  --color-bg:#f5f2ed; --color-bg-alt:#eceae4; --color-bg-card:#ffffff;
  --color-text:#1a1a18; --color-text-muted:#6b6a63; --color-text-faint:#a09f97;
  --color-border:#dedad2; --color-accent:#d95f2b; --color-accent-hover:#c2521f;
  --color-accent-soft:#faeee7;
  --font-sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
  --text-sm:0.875rem; --text-base:1rem; --text-lg:1.125rem; --text-xl:1.25rem;
  --text-2xl:1.5rem; --text-3xl:1.875rem;
  --weight-medium:500; --weight-semibold:600; --weight-bold:700;
  --space-2:0.5rem; --space-3:0.75rem; --space-4:1rem; --space-5:1.25rem;
  --space-6:1.5rem; --space-8:2rem; --space-12:3rem;
  --radius-md:8px; --radius-lg:12px;
  --shadow-sm:0 1px 3px rgba(0,0,0,0.07); --shadow-md:0 4px 12px rgba(0,0,0,0.1);
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{font-family:var(--font-sans);background:var(--color-bg);color:var(--color-text);min-height:100vh}
header{background:var(--color-bg-card);border-bottom:1px solid var(--color-border);padding:var(--space-6) var(--space-8);display:flex;align-items:center;gap:var(--space-4);}
header h1{font-size:var(--text-2xl);font-weight:var(--weight-bold);}
header .meta{font-size:var(--text-sm);color:var(--color-text-faint);margin-left:auto}
.container{max-width:1100px;margin:0 auto;padding:var(--space-8)}
.search input{
  padding:var(--space-2) var(--space-4);border:1px solid var(--color-border);
  border-radius:var(--radius-md);font-size:var(--text-sm);background:var(--color-bg-card);
  color:var(--color-text);outline:none;width:220px;
}
.search input:focus{border-color:var(--color-accent)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:var(--space-6)}
.card-wrap{display:flex;flex-direction:column;gap:var(--space-3);}
.card{
  background:var(--color-bg-card);border:1px solid var(--color-border);border-radius:var(--radius-lg);
  text-decoration:none;color:inherit;display:flex;flex-direction:column;overflow:hidden;
  box-shadow:var(--shadow-sm);transition:all 180ms ease;
}
.card:hover{box-shadow:var(--shadow-md);border-color:var(--color-accent);transform:translateY(-2px)}
.card-thumb{position:relative;width:100%;height:180px;overflow:hidden;flex-shrink:0;}
.card-thumb img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;}
.card-thumb-grad{/* gradient set inline */}
.card-thumb-glass{position:absolute;inset:0;background:rgba(5,5,10,0.36);}
.card-body{padding:var(--space-6);height:132px;overflow:hidden;display:flex;flex-direction:column;gap:var(--space-2);flex-shrink:0;}
.card-header{display:flex;align-items:center;justify-content:space-between;flex-shrink:0;}
.card-folder{font-size:var(--text-sm);font-weight:var(--weight-medium);color:var(--color-accent);background:var(--color-accent-soft);padding:3px var(--space-3);border-radius:var(--radius-md);}
.card-date{font-size:var(--text-sm);color:var(--color-text-faint)}
.card-title{font-size:var(--text-base);font-weight:var(--weight-semibold);line-height:1.5;letter-spacing:-0.01em;color:var(--color-text);display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;}
.card-desc{font-size:var(--text-sm);color:var(--color-text-muted);line-height:1.7;padding:0 var(--space-1);}
.empty{text-align:center;color:var(--color-text-faint);padding:var(--space-12);font-size:var(--text-lg)}
footer{text-align:center;padding:var(--space-8);color:var(--color-text-faint);font-size:var(--text-sm);border-top:1px solid var(--color-border);margin-top:var(--space-12)}
@media(max-width:600px){
  header{padding:var(--space-4)}.container{padding:var(--space-4)}
  .search input{width:100%}
}
@media(max-width:700px){
  :root{
    --text-sm:1rem;
    --text-base:1.15rem;
    --text-lg:1.35rem;
    --text-xl:1.55rem;
    --text-2xl:1.85rem;
    --text-3xl:2.25rem;
  }
}
"""


# ── Card HTML rendering ──────────────────────────────────────────────────────

def render_cards(files, label, gradients, path_prefix=""):
    html = ""
    for idx, f in enumerate(files):
        date_str = f"<span class='card-date'>{f['date']}</span>" if f["date"] else ""
        desc_str = f"<p class='card-desc'>{f['description']}</p>" if f["description"] else ""
        href = path_prefix + f["name"] if path_prefix else f["name"]
        c1, c2 = gradients[idx % len(gradients)]
        if f["og_image"]:
            thumb = (
                f"<div class='card-thumb'>"
                f"<img src='{f['og_image']}' alt='' loading='lazy'>"
                f"<div class='card-thumb-glass'></div></div>"
            )
        else:
            thumb = (
                f"<div class='card-thumb card-thumb-grad'"
                f" style='background:linear-gradient(135deg,#{c1},#{c2})'>"
                f"<div class='card-thumb-glass'></div></div>"
            )
        html += f"""
    <div class="card-wrap">
      <a class="card" href="{href}">
        {thumb}
        <div class="card-body">
          <div class="card-header">
            <span class="card-folder">{label}</span>
            {date_str}
          </div>
          <h3 class="card-title">{f['title']}</h3>
        </div>
      </a>
      {desc_str}
    </div>"""
    return html


# ── Main index (category cards) ──────────────────────────────────────────────

def build_main_index(folders):
    generated = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    total = sum(len(v) for v in folders.values())

    cat_cards_html = ""
    for key, meta in CATEGORY_META.items():
        files = folders.get(key, [])
        count = len(files)
        preview_items = "".join(
            f"<li>{f['title']}</li>" for f in files[:3]
        )
        cat_cards_html += f"""
    <a class="cat-card" href="{key}/index.html">
      <div class="cat-thumb" style="background:linear-gradient(135deg,#{meta['grad_from']},#{meta['grad_to']})">
        <div class="cat-name">{meta['label']}</div>
      </div>
      <div class="cat-body">
        <p class="cat-desc">{meta['description']}</p>
        <div class="cat-count">{count}개 아티클</div>
        <ul class="cat-preview">{preview_items}</ul>
        <span class="cat-more">모두 보기 →</span>
      </div>
    </a>"""

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>My HTML Library</title>
<link rel="manifest" href="manifest.json">
<meta name="theme-color" content="#d95f2b">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<meta name="apple-mobile-web-app-title" content="HTML Library">
<style>
{SHARED_CSS}
/* Category cards */
.cat-grid{{display:grid;grid-template-columns:1fr 1fr;gap:var(--space-8);margin-top:var(--space-8);}}
.cat-card{{
  background:var(--color-bg-card);border:1px solid var(--color-border);border-radius:var(--radius-lg);
  overflow:hidden;text-decoration:none;color:inherit;
  box-shadow:var(--shadow-sm);transition:all 200ms ease;display:flex;flex-direction:column;
}}
.cat-card:hover{{box-shadow:var(--shadow-md);transform:translateY(-4px);border-color:transparent;}}
.cat-thumb{{
  height:160px;display:flex;align-items:flex-end;padding:var(--space-6);
  position:relative;
}}
.cat-name{{
  font-size:var(--text-3xl);font-weight:var(--weight-bold);color:#fff;
  letter-spacing:-0.02em;text-shadow:0 1px 6px rgba(0,0,0,0.25);
}}
.cat-body{{padding:var(--space-6);flex:1;display:flex;flex-direction:column;gap:var(--space-4);}}
.cat-desc{{font-size:var(--text-sm);color:var(--color-text-muted);}}
.cat-count{{font-size:var(--text-sm);font-weight:var(--weight-semibold);color:var(--color-accent);}}
.cat-preview{{list-style:none;display:flex;flex-direction:column;gap:var(--space-2);}}
.cat-preview li{{
  font-size:var(--text-sm);color:var(--color-text);
  display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical;overflow:hidden;
  padding-left:var(--space-3);border-left:2px solid var(--color-border);
  line-height:1.5;
}}
.cat-more{{margin-top:auto;font-size:var(--text-sm);font-weight:var(--weight-semibold);color:var(--color-accent);padding-top:var(--space-2);}}
.page-subtitle{{font-size:var(--text-base);color:var(--color-text-muted);margin-top:var(--space-3);}}
@media(max-width:700px){{
  .cat-grid{{grid-template-columns:1fr;gap:var(--space-6);}}
  .cat-thumb{{height:120px;}}
  .cat-name{{font-size:var(--text-2xl);}}
}}
</style>
</head>
<body>
<header>
  <h1>My HTML Library</h1>
  <span class="meta">{total} articles · {generated}</span>
</header>
<div class="container">
  <p class="page-subtitle">주제를 선택하면 관련 아티클을 볼 수 있습니다.</p>
  <div class="cat-grid">
    {cat_cards_html}
  </div>
</div>
<footer>Generated by GitHub Actions · <a href="design-system.html" style="color:var(--color-accent)">Design System</a></footer>
<script>
if ('serviceWorker' in navigator) {{
  navigator.serviceWorker.register('/my-html/sw.js');
}}
</script>
</body>
</html>
"""


# ── Sub-index (per category) ─────────────────────────────────────────────────

def build_sub_index(key, files):
    meta = CATEGORY_META[key]
    generated = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    cards = render_cards(files, meta["label"], meta["gradients"])
    count = len(files)

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{meta['label']} — My HTML Library</title>
<style>
{SHARED_CSS}
.breadcrumb{{display:flex;align-items:center;gap:var(--space-2);font-size:var(--text-sm);color:var(--color-text-muted);}}
.breadcrumb a{{color:var(--color-text-muted);text-decoration:none;}}
.breadcrumb a:hover{{color:var(--color-accent);}}
.breadcrumb-sep{{color:var(--color-text-faint);}}
.cat-header{{margin-bottom:var(--space-6);}}
.cat-header h2{{
  font-size:var(--text-3xl);font-weight:var(--weight-bold);
  background:linear-gradient(135deg,#{meta['grad_from']},#{meta['grad_to']});
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  background-clip:text;margin:var(--space-2) 0;
}}
.cat-header p{{font-size:var(--text-base);color:var(--color-text-muted);}}
.toolbar{{display:flex;align-items:center;gap:var(--space-4);margin-bottom:var(--space-6);flex-wrap:wrap;}}
@media(max-width:600px){{.search input{{width:100%}}.toolbar{{flex-direction:column;align-items:stretch}}}}
</style>
</head>
<body>
<header>
  <div class="breadcrumb">
    <a href="../index.html">My HTML Library</a>
    <span class="breadcrumb-sep">/</span>
    <span>{meta['label']}</span>
  </div>
  <span class="meta">{count} articles · {generated}</span>
</header>
<div class="container">
  <div class="cat-header">
    <h2>{meta['label']}</h2>
    <p>{meta['description']}</p>
  </div>
  <div class="toolbar">
    <div class="search"><input type="text" placeholder="Search..." oninput="filterSearch(this.value)"></div>
  </div>
  <div class="grid" id="grid">
    {cards}
  </div>
  <div class="empty" id="empty" style="display:none">No articles found.</div>
</div>
<footer><a href="../index.html" style="color:var(--color-accent)">← My HTML Library</a> · Generated by GitHub Actions</footer>
<script>
function filterSearch(val) {{
  const q = val.toLowerCase();
  const wraps = document.querySelectorAll('.card-wrap');
  let visible = 0;
  wraps.forEach(w => {{
    const show = !q || w.textContent.toLowerCase().includes(q);
    w.style.display = show ? '' : 'none';
    if (show) visible++;
  }});
  document.getElementById('empty').style.display = visible === 0 ? '' : 'none';
}}
</script>
</body>
</html>
"""


# ── Service Worker cache version bump ────────────────────────────────────────

def bump_sw_cache(root: Path) -> None:
    sw_path = root / "sw.js"
    if not sw_path.exists():
        return
    version = datetime.utcnow().strftime("%Y%m%d-%H%M")
    text = sw_path.read_text(encoding="utf-8")
    new_text = re.sub(r"const CACHE = 'my-html-v[^']*';", f"const CACHE = 'my-html-v{version}';", text)
    if new_text != text:
        sw_path.write_text(new_text, encoding="utf-8")
        print(f"Updated sw.js cache version → my-html-v{version}")


# ── Main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Inject back buttons and mobile font scaling into category article files
    injected = 0
    fonts_injected = 0
    for category in KNOWN_CATEGORIES:
        folder_path = ROOT / category
        if not folder_path.exists():
            continue
        for html in sorted(folder_path.glob("*.html")):
            if html.name in SKIP:
                continue
            if inject_back_button(html):
                injected += 1
            if inject_mobile_fonts(html):
                fonts_injected += 1
    if injected:
        print(f"Injected back-to-index button into {injected} file(s)")
    if fonts_injected:
        print(f"Injected mobile font scaling into {fonts_injected} file(s)")

    folders = collect_files()

    # Generate sub-indexes
    for key, files in folders.items():
        sub_out = ROOT / key / "index.html"
        sub_out.write_text(build_sub_index(key, files), encoding="utf-8")
        print(f"Generated {key}/index.html — {len(files)} articles")

    # Generate main index
    main_out = ROOT / "index.html"
    main_out.write_text(build_main_index(folders), encoding="utf-8")
    total = sum(len(v) for v in folders.values())
    print(f"Generated index.html — {total} total articles across {len(folders)} categories")

    # Bump service worker cache version
    bump_sw_cache(ROOT)
