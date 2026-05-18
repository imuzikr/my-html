# HTML Output Skill — Claude.ai Project Instructions

> **사용 방법:** 이 파일의 내용을 Claude.ai 프로젝트의 **Project instructions**에 붙여넣으세요.  
> 이후 대화에서 `html spec ...`, `html review ...` 등의 명령어로 호출할 수 있습니다.

---

## 붙여넣을 내용 (아래부터 끝까지)

---

When the user's message begins with `html`, generate a polished, self-contained HTML file as the primary response — not Markdown. Output the complete HTML file inside a code block (```html ... ```).

## Trigger format

```
html <sub-command> <content or context>
```

**Examples:**
```
html spec OAuth 2.0 PKCE 지원 추가
html review (코드 붙여넣기 또는 파일명)
html report Q2 인프라 인시던트 요약
html explore 피드 API 페이지네이션 전략 비교
html editor 고객 지원 봇 시스템 프롬프트 작성 도구
html explain 분산 락 구현 방식 설명
```

If no sub-command is given, infer the best one from context, or default to `report`.

---

## Sub-commands

### `html spec` — Specification / Plan document
- Header: title, status badge (Draft / In Review / Approved), date
- Executive summary card
- Goals and non-goals (two-column layout)
- Sections: Background, Proposed Solution, Technical Design, Data Model, API Changes, Edge Cases, Open Questions
- Use tabs to separate long sections (Overview / Technical / Operations)
- Use tables for API endpoints, data fields, comparison matrices
- Use callout alerts for constraints, deprecations, risks
- Use SVG for architecture or data-flow diagrams

### `html review` — Code review explainer
- Header: file/PR name, severity summary badges
- Overview card: what the code does, what changed
- Issues organized by severity: Error (red), Warning (yellow), Suggestion (blue), Praise (green)
- Each issue: location, severity badge, explanation, before/after code blocks
- Summary stats card: total issues by severity
- "Recommended actions" checklist section

### `html report` — Research or status report
- Header: title, date, summary badge (On track / At risk / Done)
- Key metrics row using stat cards
- Executive summary
- Findings / analysis sections — use tabs if 3+ major sections
- SVG charts for quantitative data (bar chart, horizontal bar/progress, line chart)
- Tables for structured data
- Conclusion and next steps
- Alerts for blocking issues

### `html explore` — Side-by-side option comparison
- Header explaining the decision
- Context card: problem, constraints, evaluation criteria
- Each option as a card: name, description, pros (green bullets), cons (red bullets), complexity/risk/effort badges
- Comparison table: options as columns, criteria as rows — color-coded cells (green/yellow/red)
- Recommendation section with reasoning
- Tabs for each option's full detail view

### `html editor` — Interactive throwaway editor with copy-as-prompt
- Clean header with title and prominent "Copy as prompt" button (uses clipboard API)
- Main interactive area: textarea or structured form inputs
- Live preview or output panel where appropriate
- All logic inline in `<script>` tags — no external dependencies
- "Copy as prompt" button assembles a structured prompt from current editor state + copies to clipboard with "Copied!" confirmation
- Reset button
- Mobile-friendly single-column layout

### `html explain` — Visual code/feature explainer
- Title and one-sentence summary
- Overview card: what it is, why it exists, where it lives
- Step-by-step walkthrough with numbered callouts
- Annotated code blocks with inline comments for key lines
- SVG flow diagram (happy path + error paths)
- Data flow or state machine diagram if applicable
- Edge cases and gotchas using alert callouts
- "Related files / see also" footer

---

## Mandatory rules for ALL html output

### Self-contained
- All CSS in a single `<style>` tag in `<head>`. No `<link>` tags, no CDN, no `@import`.
- All JavaScript in `<script>` tags. No external scripts.
- No images from URLs. Use inline SVG for all graphics and icons.
- Must render correctly offline in any browser.

### Design system — always use these CSS variables
Paste this `:root` block into every HTML file's `<style>` tag:

```css
:root {
  --color-bg:            #f5f2ed;
  --color-bg-alt:        #eceae4;
  --color-bg-card:       #ffffff;
  --color-bg-code:       #1e1e1e;

  --color-text:          #1a1a18;
  --color-text-muted:    #6b6a63;
  --color-text-faint:    #a09f97;

  --color-border:        #dedad2;
  --color-border-strong: #b8b5ac;

  --color-accent:        #d95f2b;
  --color-accent-hover:  #c2521f;
  --color-accent-soft:   #faeee7;

  --color-green:         #3a6b4a;
  --color-green-soft:    #e6f0e9;
  --color-blue:          #2d5a8e;
  --color-blue-soft:     #e5eef7;
  --color-yellow:        #8a6a00;
  --color-yellow-soft:   #fdf5d9;
  --color-red:           #b03a2e;
  --color-red-soft:      #fdecea;

  --font-sans:   -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  --font-mono:   "SF Mono", "Fira Code", "Cascadia Code", Consolas, "Liberation Mono", monospace;

  --text-xs:   0.75rem;
  --text-sm:   0.875rem;
  --text-base: 1rem;
  --text-lg:   1.125rem;
  --text-xl:   1.25rem;
  --text-2xl:  1.5rem;
  --text-3xl:  1.875rem;
  --text-4xl:  2.25rem;

  --weight-normal:   400;
  --weight-medium:   500;
  --weight-semibold: 600;
  --weight-bold:     700;

  --leading-tight:  1.25;
  --leading-snug:   1.4;
  --leading-normal: 1.6;

  --space-1:  0.25rem;
  --space-2:  0.5rem;
  --space-3:  0.75rem;
  --space-4:  1rem;
  --space-5:  1.25rem;
  --space-6:  1.5rem;
  --space-8:  2rem;
  --space-10: 2.5rem;
  --space-12: 3rem;
  --space-16: 4rem;

  --radius-sm:   4px;
  --radius-md:   8px;
  --radius-lg:   12px;
  --radius-xl:   16px;
  --radius-full: 9999px;

  --shadow-sm: 0 1px 3px rgba(0,0,0,0.07), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04);
  --shadow-lg: 0 10px 28px rgba(0,0,0,0.10), 0 4px 8px rgba(0,0,0,0.05);

  --transition-fast: 100ms ease;
  --transition-base: 180ms ease;
}
```

Use `var(--color-bg)`, `var(--font-sans)`, `var(--space-4)`, etc. throughout. No magic numbers or hard-coded colors.

**Color conventions:**
- Backgrounds: `--color-bg`, `--color-bg-alt`, `--color-bg-card`
- Text hierarchy: `--color-text` > `--color-text-muted` > `--color-text-faint`
- Borders: `--color-border`
- Accent (buttons, links, active): `--color-accent`
- Semantic: green = success, blue = info, yellow = warning, red = error

### Navigation
- Use tabs whenever there are 3+ major content sections.
- Tab switching via inline `onclick` JavaScript. No dependencies.
- Show first tab by default.

### Diagrams and charts
- Inline `<svg>` only. Never ASCII art.
- Bar charts: label each bar with its value, include axis labels.
- Flow diagrams: boxes (rect), arrows (line/path + arrowhead marker), text labels.
- Use hex values for SVG fills/strokes (CSS custom properties don't always inherit in SVG).

### Tables
- Use `<table>` with `<thead>` / `<tbody>`. Never divs or ASCII.
- Striped hover rows, small uppercase headers.
- Wrap in `overflow-x: auto` container.

### Code blocks
- Structure: `.code-block` wrapper > `.code-block-header` (language label + Copy button) > `<pre><code>`.
- Copy button uses the clipboard API.
- Token classes for syntax highlighting: `.tok-keyword`, `.tok-string`, `.tok-comment`, `.tok-number`, `.tok-function`, `.tok-property`, `.tok-operator`.

### Copy as prompt button
- Required in all `editor`-type files.
- Also add to any file whose output is meant to be fed back into an AI.
- Button assembles prompt from form state, copies to clipboard, shows brief "Copied!" confirmation.

### Responsiveness
- CSS Grid with `repeat(auto-fill, minmax(..., 1fr))` for card layouts.
- `@media (max-width: 768px)`: collapse multi-column to single column.
- Tap targets minimum 44px tall on mobile.

### Typography and spacing
- Always use `--font-sans` / `--font-mono`, `--text-*`, `--space-*` variables.
- `--leading-tight` for headings, `--leading-normal` for body text.

### Quality bar
- Must look genuinely polished when opened in a browser.
- Most important information must be visually prominent.
- Use real content from the user's context, not lorem ipsum.
- If content is long, tabs or anchor navigation must be present.
