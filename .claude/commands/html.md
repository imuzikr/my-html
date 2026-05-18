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
/html spec add real-time collaboration to the document editor
/html review src/auth/session.ts
/html report Q2 infrastructure incidents
/html explore pagination strategies for the feed API
/html editor write a system prompt for a customer support bot
/html explain how our rate limiter works
```

If no sub-command is given, choose the most appropriate one based on the content, or default to `report`.

---

## Sub-commands

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
- The "Copy as prompt" button should assemble a well-structured prompt from the current editor state and copy it to the clipboard, showing a brief "Copied!" confirmation
- A reset button
- Mobile-friendly layout (single column on narrow screens)

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

### Diagrams and charts
- Use inline `<svg>` for all diagrams, flow charts, architecture sketches, and data visualizations.
- Never use ASCII art for diagrams.
- For bar charts, label each bar with its value. Include axis labels.
- For flow diagrams, use boxes (rect), arrows (line/path with marker), and text labels.
- Charts must use the CSS color variables (pass them as `fill` or `stroke` attributes with the hex values — SVG does not inherit CSS custom properties in all contexts).

### Tables
- Use `<table>` with `<thead>` / `<tbody>` for all tabular data.
- Apply the table styles from the design system (striped hover, small uppercase headers).
- Never fake a table with divs or monospace ASCII.

### Code blocks
- Use the `.code-block` / `.code-block-header` / `<pre><code>` structure.
- Include a language label and a "Copy" button that uses the clipboard API.
- Apply token classes for syntax highlighting: `.tok-keyword`, `.tok-string`, `.tok-comment`, `.tok-number`, `.tok-function`, `.tok-property`, `.tok-operator`.

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
- Add `@media (max-width: 768px)` breakpoints to collapse multi-column layouts to single column.
- Ensure tap targets are at least 44px tall on mobile.
- Use `overflow-x: auto` on table wrappers.

### Typography and spacing
- Use the `--font-sans` and `--font-mono` variables. Never specify raw font families.
- Use `--text-*` variables for font sizes. Never use `px` or `rem` directly.
- Use `--space-*` variables for margins, padding, and gaps. Never use magic numbers.
- Line heights: `--leading-tight` for headings, `--leading-normal` for body text.

### Quality bar
- The file should look genuinely polished when opened in a browser.
- Hierarchy must be obvious at a glance: the most important information stands out.
- If content is long, navigation or tabs must be present so the user can jump around.
- Prefer real data (from the user's context) over placeholder text wherever possible.
- When generating example/placeholder values, make them realistic and domain-appropriate.

---

## Argument passing

The text after the sub-command is passed to Claude as the content or context to work with.

- For `spec` / `report` / `explore` / `explain`: treat it as the topic or subject matter.
- For `review`: treat it as a file path, diff, or pasted code.
- For `editor`: treat it as a description of the tool to build.
- If the argument references a file path, read the file first.
- If the argument is empty, ask the user for the content before generating.

---

## After generating the file

Once the HTML file has been written to disk, always run these steps automatically without asking:

### 1. Determine the save path

Use the folder that matches the sub-command:

| Sub-command | Folder |
|---|---|
| `article` / `report` / `explain` | `articles/` |
| `spec` | `specs/` |
| `review` | `reviews/` |
| `explore` | `explore/` |
| `editor` / `tools` | `tools/` |

Filename format: `YYYY-MM-DD-<slug>.html`
- Use today's date
- Derive a short kebab-case slug from the title (e.g. `2026-05-18-oauth-pkce.html`)

### 2. Commit and push to main

```bash
git add <file-path>
git commit -m "Add article: <title>"
git push origin HEAD:main
```

- Use `git push origin HEAD:main` so the push goes to main regardless of the current branch
- After a successful push, GitHub Actions will automatically regenerate `index.html` and deploy to GitHub Pages
