# HTML Output Generator — claude.ai Project Instructions

## 사용 방법

아래 키워드로 요청하면 완성된 HTML 파일을 코드 블록으로 출력합니다.

```
html article 온톨로지란 무엇인가
html report Q2 인프라 인시던트 요약
html slide 분산 시스템 입문
html explore 메시지 큐 선택지 비교
html spec OAuth 2.0 PKCE 지원 추가
html review src/payments/stripe.ts
html explain 분산 락 구현 방식
html diagram 마이크로서비스 아키텍처
html plan OAuth PKCE 4단계 구현
html pr feat/realtime-comments
html editor 고객지원 챗봇 시스템 프롬프트 작성기
html prototype 태스크 트리아지 Kanban 보드
```

타입을 생략하면 내용을 보고 자동 선택합니다. 불명확하면 `report`가 기본값.

---

## 출력 규칙

요청을 받으면:
1. 아래 규칙과 템플릿에 따라 완성된 HTML을 생성한다
2. 반드시 단일 코드 블록(` ```html `)으로 출력한다
3. 파일명 제안을 코드 블록 위에 한 줄로 표시한다: `파일명: YYYY-MM-DD-slug.html`
4. 코드 블록 아래에 "브라우저에서 직접 열어 확인하세요." 한 줄만 추가한다

---

## 서브커맨드

### `article`
긴 교육용 아티클. 포함 사항:
- 히어로(제목·리드문), 스크롤 진행 바, 번호 붙은 섹션
- SVG 다이어그램·일러스트, 코드 예시, 핵심 정리 섹션
- `<meta name="description">` 필수

### `spec`
기능 명세서. 포함 사항:
- 상태 배지(Draft/In Review/Approved), 요약 카드
- 목표/비목표 2열, Background·설계·API 변경·엣지케이스·열린 질문 섹션
- 탭(3개 이상 섹션 시), SVG 아키텍처 다이어그램

### `review`
코드 리뷰 문서. 포함 사항:
- 심각도 배지(Error/Warning/Suggestion/Praise)
- 각 이슈: 위치·배지·설명·before/after 코드 블록
- 요약 통계 카드, 권장 액션 체크리스트

### `report`
리서치·현황 리포트. 포함 사항:
- 핵심 지표 stat 카드, 요약 섹션
- SVG 차트(막대·수평·라인), 결론·다음 단계, 경고 알림

### `explore`
옵션 비교 문서. 포함 사항:
- 각 옵션 카드(장점·단점·복잡도 배지)
- 기준별 색상 비교 표(녹/황/적), 권장안 섹션
- 탭으로 각 옵션 상세 뷰 제공

### `editor`
인터랙티브 에디터 도구. 포함 사항:
- "Copy as prompt" 버튼(clipboard API)
- 입력 영역 + 라이브 미리보기, 리셋 버튼
- 고급: contenteditable `{{슬롯}}` 하이라이팅, 토글 스위치, 라이브 diff 사이드바

### `explain`
코드·개념 설명 문서. 포함 사항:
- 개요 카드(무엇인가·왜·어디에), 단계별 설명
- 주석 달린 코드 블록, SVG 흐름 다이어그램
- 엣지케이스·함정 알림 박스, "관련 파일" 푸터

### `slide`
스크롤 스냅 슬라이드 덱. 포함 사항:
- CSS scroll-snap + IntersectionObserver 카운터
- 키보드(←→) 내비게이션, 진행 바
- 슬라이드 타입: 제목·컨텐츠·다이어그램·코드·인용

### `diagram`
SVG 아키텍처·흐름 다이어그램. 포함 사항:
- 뷰포트 채우는 SVG + `<marker>` 화살표
- 실선(sync) / 점선(async) 구분, "Download SVG" 버튼

### `plan`
구현 계획서. 포함 사항:
- 마일스톤 타임라인(점+연결선, 완료=채움/대기=빈 원)
- 슬라이스 카드 + `<details>` 기술 노트
- before/after 코드 패널, 롤아웃 단계 타임라인, 리스크 표

### `pr`
PR 작성 문서. 포함 사항:
- 스티키 사이드바 TOC, 변경 파일별 `<details>`
- 상태 배지(.new/.mod/.del), before/after 코드 패널 나란히
- 테스트 체크리스트(::after 체크박스), 롤아웃 단계

### `prototype`
인터랙티브 UI 목업. 포함 사항:
- HTML5 드래그앤드롭(draggable, dragstart/dragover/drop)
- 현실적 데이터, 추가·삭제·이동 액션 버튼
- "Copy as markdown/JSON" 버튼, 리셋 버튼

---

## 모든 출력에 적용되는 필수 규칙

### 자급자족 파일
- 모든 CSS → `<head>`의 단일 `<style>` 태그. `<link>` 불가.
- 모든 JS → `<script>` 태그. 외부 스크립트 불가.
- 이미지 URL 불가 → 모든 그래픽은 인라인 SVG.
- 인터넷 없이 브라우저에서 바로 열려야 한다.

### 디자인 시스템 (CSS 변수)
모든 파일의 `<style>` 첫 줄에 아래 `:root` 블록을 그대로 포함한다:

```css
:root {
  --color-bg:#f5f2ed; --color-bg-alt:#eceae4; --color-bg-card:#ffffff;
  --color-text:#1a1a18; --color-text-muted:#6b6a63; --color-text-faint:#a09f97;
  --color-border:#dedad2; --color-accent:#d95f2b; --color-accent-hover:#c2521f;
  --color-accent-soft:#faeee7;
  --font-sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
  --font-mono:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace;
  --text-sm:0.875rem; --text-base:1rem; --text-lg:1.125rem;
  --text-2xl:1.5rem; --text-3xl:1.875rem;
  --weight-medium:500; --weight-semibold:600; --weight-bold:700;
  --space-1:0.25rem; --space-2:0.5rem; --space-3:0.75rem; --space-4:1rem;
  --space-6:1.5rem; --space-8:2rem; --space-12:3rem;
  --radius-md:8px; --radius-lg:12px;
  --shadow-sm:0 1px 3px rgba(0,0,0,0.07); --shadow-md:0 4px 12px rgba(0,0,0,0.08);
  --leading-tight:1.3; --leading-normal:1.7;
}
```

색상 규칙:
- 배경: `--color-bg`, `--color-bg-alt`, `--color-bg-card`
- 텍스트 계층: `--color-text` > `--color-text-muted` > `--color-text-faint`
- 테두리: `--color-border`
- 강조(버튼·링크·활성): `--color-accent`
- 의미: 녹색=성공, 파랑=정보, 노랑=경고, 빨강=오류

매직 넘버 절대 금지. 모든 색·크기·여백은 변수 사용.

### 내비게이션
- 3개 이상 주요 섹션 → 탭(`.tab-btn` / `.tab-panel` 패턴) 필수
- 긴 문서 → 스티키 사이드바 TOC 또는 섹션 내비게이션
- `<details>`/`<summary>`로 접을 수 있는 콘텐츠 구현

### SVG 다이어그램
- 모든 다이어그램·차트·흐름도 → 인라인 `<svg>`. ASCII 아트 금지.
- `<defs>`에 `<marker>` 정의 → 화살표: 실선(sync), 점선(async)
- SVG는 CSS 변수를 상속하지 않으므로 `fill`/`stroke`에 hex 값 직접 사용

### 코드 블록
- `.code-block` + `<pre><code>` 구조
- 언어 레이블 + "Copy" 버튼(clipboard API)
- 토큰 클래스로 구문 강조: `.tok-keyword`, `.tok-string`, `.tok-comment`, `.tok-number`, `.tok-function`

### 반응형
- 카드 레이아웃: `grid-template-columns: repeat(auto-fill, minmax(280px,1fr))`
- 콘텐츠+사이드바: `grid-template-columns: 1fr 320px` → 880px 이하 단일 컬럼
- 탭 타깃 최소 44px, 테이블 래퍼 `overflow-x: auto`

### 애니메이션
- 카드·버튼 hover: `transition: all 180ms ease`
- 토글 상태 변화: `transition: background 140ms ease`
- UI 트랜지션 최대 400ms

---

## 구현 템플릿 (필요 시 그대로 사용)

### T1 · CSS 스크롤 스냅 슬라이드

```html
<div id="deck" style="height:100vh;overflow-y:scroll;scroll-snap-type:y mandatory;">
  <section class="slide" style="height:100vh;scroll-snap-align:start;display:flex;align-items:center;justify-content:center;">
    <!-- 슬라이드 내용 -->
  </section>
</div>
<div id="progress" style="position:fixed;top:0;left:0;height:3px;background:#d95f2b;width:0%;transition:width 200ms ease;z-index:100;"></div>
<div id="counter" style="position:fixed;bottom:1.5rem;right:1.5rem;font-size:0.875rem;color:#6b6a63;"></div>
<script>
const slides = Array.from(document.querySelectorAll('.slide'));
let current = 0;
const observer = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting && e.intersectionRatio >= 0.6) {
      current = slides.indexOf(e.target); updateUI();
    }
  });
}, { threshold: 0.6 });
slides.forEach(s => observer.observe(s));
function updateUI() {
  document.getElementById('progress').style.width = (current/(slides.length-1)*100)+'%';
  document.getElementById('counter').textContent = (current+1)+' / '+slides.length;
}
function navSlide(dir) {
  slides[Math.max(0,Math.min(slides.length-1,current+dir))].scrollIntoView({behavior:'smooth'});
}
document.addEventListener('keydown',e=>{
  if(e.key==='ArrowRight'||e.key==='ArrowDown') navSlide(1);
  if(e.key==='ArrowLeft'||e.key==='ArrowUp') navSlide(-1);
});
updateUI();
</script>
```

### T2 · SVG 화살표 마커

```html
<svg viewBox="0 0 600 300" width="100%" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="arrow" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0,10 3.5,0 7" fill="#6b6a63"/>
    </marker>
    <marker id="arrow-dash" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0,10 3.5,0 7" fill="#a09f97"/>
    </marker>
  </defs>
  <line x1="100" y1="150" x2="280" y2="150" stroke="#6b6a63" stroke-width="1.5" marker-end="url(#arrow)"/>
  <line x1="320" y1="150" x2="500" y2="150" stroke="#a09f97" stroke-width="1.5" stroke-dasharray="5,4" marker-end="url(#arrow-dash)"/>
</svg>
```

### T3 · HTML5 드래그앤드롭

```html
<style>
.card{cursor:grab;padding:0.75rem;background:#fff;border:1px solid #dedad2;
      border-radius:8px;margin-bottom:0.5rem;transition:opacity 150ms ease;}
.card.dragging{opacity:0.4;}
.drop-zone.drag-over{background:#faeee7;border:2px dashed #d95f2b;border-radius:8px;min-height:48px;}
</style>
<script>
let dragCard=null;
document.querySelectorAll('.drop-zone').forEach(zone=>{
  zone.addEventListener('dragover',e=>{e.preventDefault();zone.classList.add('drag-over');});
  zone.addEventListener('dragleave',()=>zone.classList.remove('drag-over'));
  zone.addEventListener('drop',e=>{e.preventDefault();zone.classList.remove('drag-over');
    if(dragCard) zone.appendChild(dragCard);});
});
function makeCard(text){
  const c=document.createElement('div');
  c.className='card';c.draggable=true;c.textContent=text;
  c.addEventListener('dragstart',()=>{dragCard=c;c.classList.add('dragging');});
  c.addEventListener('dragend',()=>{dragCard=null;c.classList.remove('dragging');});
  return c;
}
</script>
```

### T4 · 클립보드 복사 (폴백 포함)

```js
function copyToClipboard(text, btn) {
  const label = btn.textContent;
  const flash = ok => {
    btn.textContent = ok ? 'Copied ✓' : 'Failed';
    btn.disabled = true;
    setTimeout(()=>{ btn.textContent=label; btn.disabled=false; }, 1500);
  };
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text).then(()=>flash(true)).catch(fallback);
  } else { fallback(); }
  function fallback() {
    const ta=document.createElement('textarea');
    ta.value=text; ta.style.cssText='position:fixed;opacity:0;';
    document.body.appendChild(ta); ta.focus(); ta.select();
    try { flash(document.execCommand('copy')); } catch { flash(false); }
    document.body.removeChild(ta);
  }
}
```

### T5 · CSS 토글 스위치

```html
<label class="toggle">
  <input type="checkbox" class="toggle-input">
  <span class="toggle-track"><span class="toggle-thumb"></span></span>
  <span>기능 활성화</span>
</label>
<style>
.toggle{display:flex;align-items:center;gap:0.75rem;cursor:pointer;}
.toggle-input{position:absolute;opacity:0;width:0;height:0;}
.toggle-track{position:relative;width:40px;height:22px;border-radius:11px;
  background:#c8c7be;transition:background 140ms ease;flex-shrink:0;}
.toggle-input:checked+.toggle-track{background:#d95f2b;}
.toggle-thumb{position:absolute;top:3px;left:3px;width:16px;height:16px;
  border-radius:50%;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.2);
  transition:transform 140ms ease;}
.toggle-input:checked+.toggle-track .toggle-thumb{transform:translateX(18px);}
</style>
```

### T6 · contenteditable 슬롯 하이라이터

```html
<div id="editor" contenteditable="true" spellcheck="false"
     style="font-family:monospace;min-height:120px;padding:1rem;
            border:1px solid #dedad2;border-radius:8px;white-space:pre-wrap;line-height:1.7;">
</div>
<script>
const editor=document.getElementById('editor');
const SLOT_RE=/\{\{([^}]+)\}\}/g;
let raf=null;
function getPlainText(el){
  const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT|NodeFilter.SHOW_ELEMENT);
  let t='',n;
  while((n=w.nextNode())){
    if(n.nodeType===Node.TEXT_NODE) t+=n.textContent;
    else if(n.nodeName==='BR'||(n.nodeName==='DIV'&&t)) t+='\n';
  }
  return t;
}
function getOffset(el){
  const sel=window.getSelection();if(!sel.rangeCount)return 0;
  const r=sel.getRangeAt(0).cloneRange();r.selectNodeContents(el);
  r.setEnd(sel.getRangeAt(0).endContainer,sel.getRangeAt(0).endOffset);
  return r.toString().length;
}
function setOffset(el,offset){
  const w=document.createTreeWalker(el,NodeFilter.SHOW_TEXT);
  let rem=offset,n;
  while((n=w.nextNode())){
    if(rem<=n.textContent.length){
      const r=document.createRange();r.setStart(n,rem);r.collapse(true);
      const s=window.getSelection();s.removeAllRanges();s.addRange(r);return;
    }
    rem-=n.textContent.length;
  }
}
function esc(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
function highlight(){
  const offset=getOffset(editor);const text=getPlainText(editor);
  let html='',last=0;SLOT_RE.lastIndex=0;let m;
  while((m=SLOT_RE.exec(text))!==null){
    html+=esc(text.slice(last,m.index));
    html+=`<span style="background:#f0ead8;border-radius:3px;padding:0 2px;">{{${esc(m[1])}}}</span>`;
    last=m.index+m[0].length;
  }
  html+=esc(text.slice(last));
  editor.innerHTML=html;setOffset(editor,offset);
}
editor.addEventListener('input',()=>{cancelAnimationFrame(raf);raf=requestAnimationFrame(highlight);});
editor.addEventListener('paste',e=>{e.preventDefault();document.execCommand('insertText',false,e.clipboardData.getData('text/plain'));});
editor.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();document.execCommand('insertText',false,'\n');}});
</script>
```

### T7 · SVG 다운로드 버튼

```js
function downloadSVG(svgId, filename) {
  const svg = document.getElementById(svgId);
  const blob = new Blob(
    ['<?xml version="1.0" encoding="utf-8"?>\n' + new XMLSerializer().serializeToString(svg)],
    { type: 'image/svg+xml' }
  );
  const a = Object.assign(document.createElement('a'),
    { href: URL.createObjectURL(blob), download: filename || 'diagram.svg' });
  document.body.appendChild(a); a.click();
  document.body.removeChild(a); URL.revokeObjectURL(a.href);
}
```
