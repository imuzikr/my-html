# /html — Rich HTML Output Generator

Generate a polished, self-contained HTML file instead of a Markdown response. Use this for any output that benefits from structure, navigation, interactivity, or visual hierarchy.

**Design system:** `../design-system.html` — always copy its `:root { }` CSS variables block and replicate its component styles. Do not link to it; inline everything.

---

## How to invoke

```
/html <sub-command> <content or context>
```

**Examples:**

```
/html article 온톨로지란 무엇인가
/html spec add real-time collaboration to the document editor
/html review src/auth/session.ts
/html report Q2 infrastructure incidents
/html explore pagination strategies for the feed API
/html editor write a system prompt for a customer support bot
/html explain how our rate limiter works
/html slide intro to distributed systems
/html diagram microservices architecture overview
/html plan implement OAuth 2.0 PKCE in 4 slices
/html pr feat/realtime-comments #142
/html prototype kanban board for task triage
```

If no sub-command is given, choose the most appropriate one based on the content, or default to `report`.

---

## Sub-commands

### `article`
**Write a long-form educational article**

Produce a full-length HTML article on a concept, technology, or topic. Include:
- A hero section with title, one-sentence lead, and `<meta name="description">` tag for index card previews
- Sticky nav / progress bar that tracks scroll position
- Numbered sections with clear headings and body text
- SVG diagrams or illustrations for key concepts — no ASCII art
- Annotated code examples where relevant
- A summary or "key takeaways" section at the end
- `<meta property="og:image">` if a visual thumbnail is appropriate

Filename: `articles/YYYY-MM-DD-<slug>.html`

**Example usage:** `/html article 온톨로지란 무엇인가`

---

### `spec`
**Generate a specification / plan document**

Produce a structured HTML spec for a feature, system, or change. Include:
- A header with title, status badge (Draft / In Review / Approved), author placeholder, and date
- Executive summary card
- Goals and non-goals as a clean two-column or tabbed layout
- Detailed sections: Background, Proposed Solution, Technical Design, Data Model, API Changes, Edge Cases, Open Questions
- Use tabs to separate long sections (Overview / Technical / Operations)
- Use tables for API endpoints, data fields, or comparison matrices
- Use callout alerts for important constraints, deprecations, or risks
- Use SVG diagrams for architecture or data-flow sketches

**Example usage:** `/html spec add OAuth 2.0 PKCE support to the mobile app`

---

### `review`
**Generate a code review explainer**

Produce a structured HTML code review document. Include:
- A header with the file/PR name, reviewer placeholder, severity summary badges
- Overview card: what the code does, what changed
- Issue list organized by severity: Error (red), Warning (yellow), Suggestion (blue), Praise (green)
- Each issue: location (filename + line range), severity badge, explanation paragraph, before/after code blocks with syntax highlighting
- Summary stats card: total issues, by severity
- A "Recommended actions" section with a checklist

**Example usage:** `/html review src/payments/stripe.ts`

---

### `report`
**Generate a research or status report**

Produce a polished HTML report. Include:
- A header with title, date, and summary badge (e.g., "On track", "At risk")
- Key metrics row using stat cards (--stat-card pattern)
- Executive summary section
- Findings / analysis sections — use tabs if there are 3+ major sections
- SVG charts for any quantitative data (bar chart, horizontal bar / progress, simple line chart)
- Use tables for structured data
- Conclusion and next steps section
- Alerts for any blocking issues or important callouts

**Example usage:** `/html report Q2 infrastructure incidents summary`

---

### `explore`
**Generate a side-by-side option exploration**

Produce a comparison document for evaluating approaches, tools, or designs. Include:
- A header explaining the decision being made
- Context card: the problem, constraints, and evaluation criteria
- Each option as its own card with: name, description, pros list (green bullets), cons list (red bullets), a complexity/risk/effort badge row
- A comparison table with all options as columns and criteria as rows — use colored cells (green/yellow/red) for at-a-glance scoring
- A recommendation section with reasoning

Use tabs to let the user navigate to each option's full detail view alongside the summary table.

**Example usage:** `/html explore message queue options for our notification pipeline`

---

### `editor`
**Generate a throwaway interactive editor with copy-as-prompt button**

Produce a self-contained HTML interactive editor/tool. Include:
- A clean header with title and a prominent "Copy as prompt" button (uses the clipboard API)
- The main interactive area: a `<textarea>` or structured form inputs depending on the use case
- Live preview or output panel where appropriate
- All logic inline in `<script>` tags — no external dependencies
- The "Copy as prompt" button assembles a well-structured prompt from the current editor state and copies it to the clipboard, showing a brief "Copied!" confirmation
- A reset button
- Mobile-friendly layout (single column on narrow screens)

Advanced editor patterns (apply when relevant):
- **Contenteditable + slot highlighting**: for prompt template editors, use a `contenteditable` div with `<span>` overlays to highlight `{{variable}}` placeholders in real time; preserve caret position across re-renders; use `TreeWalker` to extract clean text
- **Toggle switches**: for feature-flag or settings editors, use animated CSS toggle switches (track + animated thumb) with `transition: background 140ms ease`; show dependency warnings when required flags are disabled
- **Live diff sidebar**: when showing before/after state, render a sticky 320px sidebar with color-coded line-by-line diff (green additions, gray removals); add "Copy diff" and "Copy full JSON" buttons
- **requestAnimationFrame debouncing**: wrap live-preview updates in `requestAnimationFrame` to prevent excessive DOM operations during rapid typing
- **Event delegation**: attach a single `change` listener on the container and use `.matches()` to route events rather than binding per-element

The output must be fully functional when opened as a standalone HTML file in any browser.

**Example usage:** `/html editor write a system prompt for a customer support chatbot`

---

### `explain`
**Explain how a piece of code or feature works**

Produce a visual explainer document. Include:
- Title and one-sentence summary
- Overview card: what it is, why it exists, where it lives in the codebase
- How it works section — walk through the key logic step by step with numbered callouts
- Annotated code blocks with syntax highlighting and inline comments for key lines
- SVG flow diagram showing the happy path (and error paths if relevant)
- Data flow or state machine diagram if applicable
- Edge cases and gotchas section using alert callouts
- "Related files / see also" footer

**Example usage:** `/html explain how our distributed lock implementation works`

---

### `slide`
**Generate a presentation slide deck**

Produce a scroll-snapping slide deck where each slide fills the viewport. Include:
- CSS scroll-snap (`scroll-snap-type: y mandatory` on container; `scroll-snap-align: start` on each slide)
- Each slide is a `<section>` with `height: 100vh`; content centered with flexbox
- Keyboard navigation: left/right arrow keys scroll to prev/next slide using `scrollIntoView({ behavior: 'smooth' })`
- A slide counter in the corner updated via `IntersectionObserver` (threshold: 0.6) — not `scroll` events
- A progress bar at the top that fills as slides advance
- Slide types to mix: title slide (large serif heading + subtitle), content slide (heading + bullets), diagram slide (SVG fills most of viewport), quote slide (blockquote centered), code slide (dark background + syntax-highlighted code block)
- Consistent color theme using CSS variables; slide backgrounds alternate between `--color-bg` and `--color-bg-alt`
- Navigation arrows (prev/next buttons) fixed at bottom center; hide on first/last slide

**Example usage:** `/html slide intro to distributed systems`

---

### `diagram`
**Generate a standalone SVG architecture or flow diagram**

Produce a focused document whose main content is one or more large SVG diagrams. Include:
- A minimal header with title and optional description
- The SVG diagram fills most of the viewport; scale it with `viewBox` and `width="100%"`
- SVG elements to use: `<rect>` for boxes/services, `<circle>` for nodes, `<path>` or `<line>` for connections, `<marker>` for arrowheads (define in `<defs>`)
- Color-code by layer (e.g., client = blue, API = green, DB = orange, external = gray)
- Annotate with `<text>` labels; use `<title>` inside SVG elements for accessibility
- Add a "Download SVG" button that triggers `URL.createObjectURL(new Blob([svgContent], {type:'image/svg+xml'}))` and an `<a download>` click
- If multiple diagrams are needed, use tabs or a vertical layout with clear section headings
- Dashed lines for async/optional paths; solid lines for sync/required paths
- Arrow direction must always be clear — use `marker-end` for arrowheads

**Example usage:** `/html diagram microservices architecture overview`

---

### `plan`
**Generate an implementation plan with sliced delivery**

Produce a phased implementation document. Include:
- A header with title, delivery date, and status badge
- A milestone timeline: vertical flex column, each milestone has a filled/outlined dot + connector line, label, and date; dots are filled for completed steps, outlined for pending
- Slice / phase cards: each slice has a title, scope description, severity/effort badge, and an expandable `<details>` with technical notes
- Code panels for key technical decisions — use two-column `<details>` for before/after comparisons with a highlighted left border on the "after" side
- SVG data-flow diagram showing how components interact after the change
- A "Rollout steps" section: connected horizontal timeline (first/last child get adjusted border-radius)
- Risk / open questions table with severity badges (high = red, medium = yellow, low = green)

**Example usage:** `/html plan implement OAuth 2.0 PKCE in 4 delivery slices`

---

### `pr`
**Generate a PR writeup / code change document**

Produce a rich pull-request description document. Include:
- A header with PR title, branch name, author placeholder, and status badge (Open / Draft / Merged)
- A sticky sidebar table of contents (`position: sticky; top: 32px`) listing changed files; clicking jumps to the relevant section
- For each changed file: a `<details>` element (open by default for key files, closed for minor ones) with:
  - File path, change type badge (`.badge.new` / `.badge.mod` / `.badge.del`)
  - Before/after code panels side by side (CSS Grid `1fr 1fr`); "after" panel has olive/green border
  - Highlighted added/deleted lines with subtle background overlays
- A "Focus areas" section with numbered review guidance cards
- A "Test plan" checklist with `.done` state (custom checkbox via `::after` pseudo-element)
- A "Rollout" section showing deployment steps
- Responsive: sidebar hidden on mobile (`max-width: 900px`), file grids collapse to single column

**Example usage:** `/html pr feat/realtime-comments — real-time cursor & comment threads`

---

### `prototype`
**Generate an interactive UI prototype**

Produce a working UI mock with realistic interactions. Include:
- HTML5 drag-and-drop for reorderable lists or Kanban columns: use `draggable="true"`, `dragstart` / `dragover` / `drop` events; add `.dragging` CSS class during drag for visual feedback
- Realistic data: populate with believable items, not "Lorem ipsum"
- Action buttons that modify state: add, delete, move, mark complete
- "Export" or "Copy as markdown/JSON" button that assembles current state from the DOM and copies it to clipboard
- Status indicators: color-coded badges, progress bars, or count chips that update reactively
- A reset button that restores initial state
- Animations: `transition: all 200ms ease` on cards; use `opacity` + `transform: translateY` for enter/exit effects

Kanban-specific:
- Three columns (e.g., Backlog / In Progress / Done) in a horizontal flex layout
- Each card shows: title, priority badge, assignee initials avatar, tag chips
- Column headers show item count; count updates as cards move

**Example usage:** `/html prototype kanban board for engineering task triage`

---

## Mandatory rules for ALL /html output

Follow these rules for every HTML file generated, regardless of sub-command:

### Self-contained
- All CSS must be in a single `<style>` tag in `<head>`. No `<link>` tags, no CDN, no `@import`.
- All JavaScript must be in `<script>` tags. No external scripts.
- No images loaded from URLs. Use inline SVG for all graphics and icons.
- The file must render correctly when opened directly in a browser with no internet connection.

### Design system
- Copy the full `:root { }` CSS variables block from `../design-system.html` verbatim.
- Use `var(--color-bg)`, `var(--font-sans)`, `var(--space-4)`, etc. throughout — no magic numbers or hard-coded colors.
- Use these color conventions:
  - Backgrounds: `--color-bg`, `--color-bg-alt`, `--color-bg-card`
  - Text hierarchy: `--color-text` > `--color-text-muted` > `--color-text-faint`
  - Borders: `--color-border`
  - Accent (buttons, active states, links): `--color-accent`
  - Semantic: green = success/healthy, blue = info, yellow = warning, red = error

### Navigation
- Use tabs (`.tabs` / `.tab-btn` / `.tab-panel` pattern) whenever there are 3 or more major content sections.
- Tab switching must work with inline JavaScript (`onclick`). No dependencies.
- Always show the first tab by default.
- For very long documents, add a sticky sidebar TOC or a `position: sticky` section nav.

### Expandable sections
- Use native `<details>` / `<summary>` for collapsible content — no custom JS needed.
- Style the summary chevron with CSS `transform: rotate(90deg)` when `details[open] > summary .chevron`.
- Use `<details open>` for sections that should start expanded.

### Diagrams and charts
- Use inline `<svg>` for all diagrams, flow charts, architecture sketches, and data visualizations.
- Never use ASCII art for diagrams.
- For bar charts, label each bar with its value. Include axis labels.
- For flow diagrams, use boxes (`<rect>`), arrows (`<line>` / `<path>` with `<marker>`), and text labels.
- Define arrowheads in `<defs>` with `<marker>` elements; use `marker-end` on paths.
- Use dashed lines (`stroke-dasharray`) for optional/async connections; solid for required/sync.
- Charts must use the CSS color variables (pass them as `fill` or `stroke` attributes with the hex values — SVG does not inherit CSS custom properties in all contexts).
- Add a "Download SVG" button for standalone diagram files.

### Tables
- Use `<table>` with `<thead>` / `<tbody>` for all tabular data.
- Apply the table styles from the design system (striped hover, small uppercase headers).
- Never fake a table with divs or monospace ASCII.

### Code blocks
- Use the `.code-block` / `.code-block-header` / `<pre><code>` structure.
- Include a language label and a "Copy" button that uses the clipboard API.
- Apply token classes for syntax highlighting: `.tok-keyword`, `.tok-string`, `.tok-comment`, `.tok-number`, `.tok-function`, `.tok-property`, `.tok-operator`.
- For before/after comparisons: use two code panels side by side (CSS Grid `1fr 1fr`); highlight changed lines with a subtle background overlay; give the "after" panel a green/olive left border.

### Interactive controls
- **Toggle switches**: use a `<label>` wrapping a hidden checkbox + styled track/thumb elements; animate with `transition: background 140ms ease, transform 140ms ease`.
- **Drag-and-drop**: use `draggable="true"` + `dragstart`/`dragover`/`drop` events; add `.dragging` class for visual feedback; prevent default on `dragover` to allow drops.
- **Clipboard**: always use `navigator.clipboard.writeText()` with a `try/catch` fallback to `document.execCommand('copy')` via a temporary `<textarea>`.
- **Event delegation**: attach listeners to container elements and use `.closest()` or `.matches()` to route events rather than binding per-element.

### Copy as prompt button
- Every `editor`-type file must have a "Copy as prompt" button.
- Any file where the output is meant to be fed back into an AI should have this button.
- Button template:
  ```html
  <button class="btn btn-primary" onclick="copyPrompt()">
    <svg ...><!-- clipboard icon --></svg>
    Copy as prompt
  </button>
  ```
  ```js
  function copyPrompt() {
    const prompt = buildPrompt(); // assemble from form state
    navigator.clipboard.writeText(prompt).then(() => {
      // brief visual confirmation
    });
  }
  ```

### Responsiveness
- Use CSS Grid with `grid-template-columns: repeat(auto-fill, minmax(..., 1fr))` for card layouts.
- For content + sidebar layouts use `grid-template-columns: 1fr 320px`; collapse to single column below 880px.
- Add `@media (max-width: 768px)` breakpoints to collapse multi-column layouts to single column.
- Ensure tap targets are at least 44px tall on mobile.
- Use `overflow-x: auto` on table wrappers.
- Hide decorative sidebars entirely on mobile (`display: none` below breakpoint).

### Typography and spacing
- Use the `--font-sans` and `--font-mono` variables. Never specify raw font families.
- Use `--text-*` variables for font sizes. Never use `px` or `rem` directly.
- Use `--space-*` variables for margins, padding, and gaps. Never use magic numbers.
- Line heights: `--leading-tight` for headings, `--leading-normal` for body text.

### Animations and transitions
- Use CSS transitions for hover states: `transition: all 180ms ease` on cards, buttons, and interactive elements.
- Use `opacity` + `transform: translateY(-4px)` for subtle hover lift effects.
- Slide/enter animations: `@keyframes` with `opacity 0→1` + `transform translateY(8px)→0`.
- Never use `animation-duration` longer than 400ms for UI transitions — keep them snappy.
- Use `transition: background 140ms ease` for color state changes (toggles, active tabs).

### Semantic HTML
- Use `<details>` / `<summary>` for collapsible content.
- Use `<nav>` for table of contents and tab navigation.
- Use `<article>` for self-contained content blocks.
- Use `<aside>` for sidebars.
- Add `aria-label` and `title` attributes on interactive SVG elements.
- Add `loading="lazy"` on any `<img>` tags.

### Quality bar
- The file should look genuinely polished when opened in a browser.
- Hierarchy must be obvious at a glance: the most important information stands out.
- If content is long, navigation or tabs must be present so the user can jump around.
- Prefer real data (from the user's context) over placeholder text wherever possible.
- When generating example/placeholder values, make them realistic and domain-appropriate.
- Interactive features must actually work — test the logic mentally before writing it.

---

## Implementation templates

Copy these verbatim when the pattern is needed. Do not rewrite from memory.

---

### T1 · CSS scroll-snap slide deck

```html
<!-- Container -->
<div id="deck" style="height:100vh;overflow-y:scroll;scroll-snap-type:y mandatory;">
  <section class="slide" style="height:100vh;scroll-snap-align:start;display:flex;align-items:center;justify-content:center;">
    <!-- slide content -->
  </section>
  <!-- repeat <section class="slide"> for each slide -->
</div>

<!-- Progress bar -->
<div id="progress" style="position:fixed;top:0;left:0;height:3px;background:var(--color-accent);width:0%;transition:width 200ms ease;z-index:100;"></div>

<!-- Slide counter -->
<div id="counter" style="position:fixed;bottom:1.5rem;right:1.5rem;font-size:var(--text-sm);color:var(--color-text-muted);"></div>

<!-- Prev / Next buttons -->
<button id="btn-prev" onclick="navSlide(-1)" style="position:fixed;bottom:1.5rem;left:50%;transform:translateX(-60px);...">&#8592;</button>
<button id="btn-next" onclick="navSlide(1)"  style="position:fixed;bottom:1.5rem;left:50%;transform:translateX(12px);...">&#8594;</button>

<script>
const slides = Array.from(document.querySelectorAll('.slide'));
let current = 0;

// IntersectionObserver — do NOT use scroll events
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting && e.intersectionRatio >= 0.6) {
      current = slides.indexOf(e.target);
      updateUI();
    }
  });
}, { threshold: 0.6 });
slides.forEach(s => observer.observe(s));

function updateUI() {
  const pct = slides.length > 1 ? (current / (slides.length - 1)) * 100 : 100;
  document.getElementById('progress').style.width = pct + '%';
  document.getElementById('counter').textContent = (current + 1) + ' / ' + slides.length;
  document.getElementById('btn-prev').style.opacity = current === 0 ? '0' : '1';
  document.getElementById('btn-next').style.opacity = current === slides.length - 1 ? '0' : '1';
}

function navSlide(dir) {
  const next = Math.max(0, Math.min(slides.length - 1, current + dir));
  slides[next].scrollIntoView({ behavior: 'smooth' });
}

// Keyboard navigation
document.addEventListener('keydown', e => {
  if (e.key === 'ArrowRight' || e.key === 'ArrowDown') navSlide(1);
  if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')   navSlide(-1);
});

updateUI();
</script>
```

---

### T2 · SVG arrowhead marker

```html
<svg width="600" height="300" viewBox="0 0 600 300" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <!-- solid arrow (sync / required) -->
    <marker id="arrow" markerWidth="10" markerHeight="7"
            refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#6b6a63"/>
    </marker>
    <!-- dashed arrow (async / optional) -->
    <marker id="arrow-dashed" markerWidth="10" markerHeight="7"
            refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#a09f97"/>
    </marker>
  </defs>

  <!-- Solid connection -->
  <line x1="100" y1="150" x2="280" y2="150"
        stroke="#6b6a63" stroke-width="1.5" marker-end="url(#arrow)"/>

  <!-- Dashed connection (async) -->
  <line x1="320" y1="150" x2="500" y2="150"
        stroke="#a09f97" stroke-width="1.5" stroke-dasharray="5,4"
        marker-end="url(#arrow-dashed)"/>

  <!-- Box -->
  <rect x="20" y="120" width="80" height="40" rx="6"
        fill="#ffffff" stroke="#dedad2" stroke-width="1.5"/>
  <text x="60" y="145" text-anchor="middle" font-size="12" fill="#1a1a18">Service A</text>
</svg>
```

---

### T3 · HTML5 drag-and-drop (Kanban columns)

```html
<div class="board" style="display:flex;gap:var(--space-4);">
  <div class="column" data-col="backlog">
    <h3>Backlog <span class="count">0</span></h3>
    <div class="drop-zone"></div>
  </div>
  <div class="column" data-col="in-progress">
    <h3>In Progress <span class="count">0</span></h3>
    <div class="drop-zone"></div>
  </div>
  <div class="column" data-col="done">
    <h3>Done <span class="count">0</span></h3>
    <div class="drop-zone"></div>
  </div>
</div>

<style>
.card { cursor: grab; padding: var(--space-3); background: var(--color-bg-card);
        border: 1px solid var(--color-border); border-radius: var(--radius-md);
        margin-bottom: var(--space-2); transition: opacity 150ms ease; }
.card.dragging { opacity: 0.4; cursor: grabbing; }
.drop-zone.drag-over { background: var(--color-accent-soft);
                        border: 2px dashed var(--color-accent); border-radius: var(--radius-md); }
</style>

<script>
let dragCard = null;

document.querySelectorAll('.drop-zone').forEach(zone => {
  zone.addEventListener('dragover', e => {
    e.preventDefault();                        // must preventDefault to allow drop
    zone.classList.add('drag-over');
  });
  zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
  zone.addEventListener('drop', e => {
    e.preventDefault();
    zone.classList.remove('drag-over');
    if (dragCard) { zone.appendChild(dragCard); updateCounts(); }
  });
});

function makeCard(text, priority = 'normal') {
  const card = document.createElement('div');
  card.className = 'card';
  card.draggable = true;
  card.innerHTML = `<span>${text}</span>`;
  card.addEventListener('dragstart', () => { dragCard = card; card.classList.add('dragging'); });
  card.addEventListener('dragend',   () => { dragCard = null; card.classList.remove('dragging'); });
  return card;
}

function updateCounts() {
  document.querySelectorAll('.column').forEach(col => {
    col.querySelector('.count').textContent = col.querySelectorAll('.card').length;
  });
}
</script>
```

---

### T4 · Clipboard with execCommand fallback

```js
function copyToClipboard(text, btn) {
  const restore = btn.textContent;
  const flash = ok => {
    btn.textContent = ok ? 'Copied ✓' : 'Failed';
    btn.disabled = true;
    setTimeout(() => { btn.textContent = restore; btn.disabled = false; }, 1500);
  };

  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(() => flash(true)).catch(() => fallback());
  } else {
    fallback();
  }

  function fallback() {
    const ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;opacity:0;top:0;left:0;';
    document.body.appendChild(ta);
    ta.focus(); ta.select();
    try { flash(document.execCommand('copy')); }
    catch { flash(false); }
    document.body.removeChild(ta);
  }
}
```

---

### T5 · CSS toggle switch

```html
<label class="toggle">
  <input type="checkbox" class="toggle-input">
  <span class="toggle-track">
    <span class="toggle-thumb"></span>
  </span>
  <span class="toggle-label">Enable feature</span>
</label>

<style>
.toggle { display:flex; align-items:center; gap:var(--space-3); cursor:pointer; }
.toggle-input { position:absolute; opacity:0; width:0; height:0; }
.toggle-track {
  position:relative; width:40px; height:22px; border-radius:11px;
  background:#c8c7be; transition:background 140ms ease; flex-shrink:0;
}
.toggle-input:checked + .toggle-track { background:var(--color-accent); }
.toggle-thumb {
  position:absolute; top:3px; left:3px;
  width:16px; height:16px; border-radius:50%;
  background:#fff; box-shadow:0 1px 3px rgba(0,0,0,.2);
  transition:transform 140ms ease;
}
.toggle-input:checked + .toggle-track .toggle-thumb { transform:translateX(18px); }
.toggle-input:focus-visible + .toggle-track { outline:2px solid var(--color-accent); outline-offset:2px; }
</style>
```

---

### T6 · contenteditable prompt editor with slot highlighting

```html
<div id="editor" contenteditable="true" spellcheck="false"
     style="font-family:var(--font-mono);min-height:160px;padding:var(--space-4);
            border:1px solid var(--color-border);border-radius:var(--radius-md);
            outline:none;white-space:pre-wrap;line-height:1.7;">
</div>

<script>
const editor = document.getElementById('editor');
const SLOT_RE = /\{\{([^}]+)\}\}/g;
let raf = null;

// Extract plain text (handles browser-injected <div>/<br> on Enter)
function getPlainText(el) {
  const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT);
  let text = '', node;
  while ((node = walker.nextNode())) {
    if (node.nodeType === Node.TEXT_NODE) {
      text += node.textContent;
    } else if (node.nodeName === 'BR' || (node.nodeName === 'DIV' && text)) {
      text += '\n';
    }
  }
  return text;
}

// Save and restore caret position by character offset
function getCaretOffset(el) {
  const sel = window.getSelection();
  if (!sel.rangeCount) return 0;
  const range = sel.getRangeAt(0).cloneRange();
  range.selectNodeContents(el);
  range.setEnd(sel.getRangeAt(0).endContainer, sel.getRangeAt(0).endOffset);
  return range.toString().length;
}

function setCaretOffset(el, offset) {
  const walker = document.createTreeWalker(el, NodeFilter.SHOW_TEXT);
  let remaining = offset, node;
  while ((node = walker.nextNode())) {
    if (remaining <= node.textContent.length) {
      const range = document.createRange();
      range.setStart(node, remaining);
      range.collapse(true);
      const sel = window.getSelection();
      sel.removeAllRanges();
      sel.addRange(range);
      return;
    }
    remaining -= node.textContent.length;
  }
}

function highlight() {
  const offset = getCaretOffset(editor);
  const text = getPlainText(editor);

  // Build highlighted HTML
  let html = '', last = 0;
  SLOT_RE.lastIndex = 0;
  let m;
  while ((m = SLOT_RE.exec(text)) !== null) {
    html += escHtml(text.slice(last, m.index));
    html += `<span style="background:#f0ead8;border-radius:3px;padding:0 2px;">\{\{${escHtml(m[1])}\}\}</span>`;
    last = m.index + m[0].length;
  }
  html += escHtml(text.slice(last));

  editor.innerHTML = html;
  setCaretOffset(editor, offset);
}

function escHtml(s) {
  return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
}

editor.addEventListener('input', () => {
  cancelAnimationFrame(raf);
  raf = requestAnimationFrame(highlight);
});

// Paste as plain text only
editor.addEventListener('paste', e => {
  e.preventDefault();
  const text = e.clipboardData.getData('text/plain');
  document.execCommand('insertText', false, text);
});

// Insert real newline on Enter (prevent nested divs)
editor.addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    e.preventDefault();
    document.execCommand('insertText', false, '\n');
  }
});
</script>
```

---

### T7 · SVG download button

```js
function downloadSVG(svgId, filename) {
  const svg = document.getElementById(svgId);
  const serializer = new XMLSerializer();
  const svgStr = '<?xml version="1.0" encoding="utf-8"?>\n' + serializer.serializeToString(svg);
  const blob = new Blob([svgStr], { type: 'image/svg+xml' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url; a.download = filename || 'diagram.svg';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
```

```html
<button onclick="downloadSVG('my-diagram', 'architecture.svg')"
        style="display:inline-flex;align-items:center;gap:var(--space-2);...">
  <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
    <path d="M8 2v8M5 7l3 3 3-3M2 12h12" stroke="currentColor" stroke-width="1.5"
          stroke-linecap="round" stroke-linejoin="round"/>
  </svg>
  Download SVG
</button>
```

---

## Argument passing

The text after the sub-command is passed to Claude as the content or context to work with.

- For `article` / `spec` / `report` / `explore` / `explain` / `slide` / `diagram` / `plan`: treat it as the topic or subject matter.
- For `review` / `pr`: treat it as a file path, diff, PR number, or pasted code.
- For `editor` / `prototype`: treat it as a description of the tool or UI to build.
- If the argument references a file path, read the file first.
- If the argument is empty, ask the user for the content before generating.

---

## After generating the file

Once the HTML file has been written to disk:

### 1. Determine the save path

Use the folder that matches the sub-command:

| Sub-command | Folder |
|---|---|
| `article` / `report` / `explain` | `articles/` |
| `spec` / `plan` | `specs/` |
| `review` / `pr` | `reviews/` |
| `explore` | `explore/` |
| `editor` / `prototype` / `tools` / `slide` | `tools/` |
| `diagram` | `articles/` |

Filename format: `YYYY-MM-DD-<slug>.html`
- Use today's date
- Derive a short kebab-case slug from the title (e.g. `2026-05-18-oauth-pkce.html`)

### 2. Review before publishing

After saving the file, **do not commit or push immediately**. First give the user the generated file path and a concrete way to review it, such as a local file path, preview URL, or screenshot if available.

Ask for explicit approval before committing and pushing:

> 파일이 저장되었습니다: `articles/YYYY-MM-DD-slug.html`
> 먼저 내용을 확인해 주세요. 확인 후 배포하려면 "푸시해 주세요", "배포해 주세요", or "승인합니다"라고 답해 주세요.

Only if the user explicitly approves publishing, run:

```bash
git add <file-path>
git commit -m "Add article: <title>"
git push origin HEAD:main
```

- Do not treat "make an HTML file" as approval to publish.
- Treat "make and deploy", "push it", "배포해 주세요", "푸시해 주세요", or "승인합니다" as publishing approval only after the generated result has been presented for review in the current turn.
- Use `git push origin HEAD:main` so the push goes to main regardless of the current branch
- After a successful push, GitHub Actions will automatically regenerate `index.html` and deploy to GitHub Pages
