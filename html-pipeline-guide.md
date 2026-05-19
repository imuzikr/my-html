# HTML 자동 발행 파이프라인 — 스킬과 GitHub Actions 완전 가이드

## 시스템 개요

이 파이프라인은 **AI가 HTML 아티클을 작성하면 자동으로 웹에 발행되는 시스템**이다.  
글쓴이가 신경 써야 할 일은 주제를 정하고 결과를 확인하는 것뿐이다.

```
주제 입력 → AI 생성 → 검토 후 확인 → git push
                                              ↓
웹 공개 완료 ← GitHub Pages 배포 ← 목차 재생성 ← GitHub Actions 실행
```

이 파이프라인은 두 축으로 구성된다.

- **/html 스킬** — AI가 아티클을 만드는 방법을 정의
- **GitHub Actions 파이프라인** — 만들어진 파일을 자동으로 배포

---

## /html 스킬

Claude Code의 슬래시 커맨드로 등록된 스킬이다.  
`.claude/commands/html.md` 파일이 그 정의이며, 호출하면 Claude가 이 규칙에 따라 HTML을 생성한다.

### 사용법

```
/html <sub-command> <주제 또는 내용>
```

### Sub-command 목록

| Sub-command | 용도 | 저장 폴더 | 예시 |
|---|---|---|---|
| `article` | 일반 글·해설 | articles/ | `/html article 온톨로지란 무엇인가` |
| `report` | 분석·현황 리포트 | articles/ | `/html report Q2 인프라 인시던트` |
| `spec` | 기능 명세서 | specs/ | `/html spec OAuth 2.0 PKCE 지원 추가` |
| `review` | 코드 리뷰 문서 | reviews/ | `/html review src/auth/session.ts` |
| `explore` | 옵션 비교·탐색 | explore/ | `/html explore 메시지 큐 선택지` |
| `explain` | 코드·개념 설명 | articles/ | `/html explain 분산 락 구현 방식` |
| `editor` | 인터랙티브 도구 | tools/ | `/html editor 시스템 프롬프트 작성기` |

> sub-command를 생략하면 내용을 보고 Claude가 자동으로 선택한다. 명확하지 않을 때는 `report`가 기본값.

### 생성 규칙 (html.md가 정의하는 것)

| 규칙 | 내용 |
|---|---|
| 자급자족 파일 | CSS·JS를 모두 인라인으로 포함. 외부 의존성 없음 |
| 디자인 시스템 준수 | design-system.html의 CSS 변수 블록 사용 |
| SVG 다이어그램 | 모든 도식은 인라인 SVG. 이미지 URL 사용 금지 |
| 파일명 규칙 | `YYYY-MM-DD-slug.html` (날짜 + 케밥케이스 슬러그) |
| 반응형 | 모바일 768px 기준 단일 컬럼 전환 |
| 푸시 확인 | 파일 저장 후 배포 여부를 사용자에게 물어봄 |

---

## GitHub Actions 파이프라인

main 브랜치에 푸시되는 순간 자동으로 실행되는 워크플로다.

### deploy.yml

```yaml
name: Build & Deploy to GitHub Pages

on:
  push:
    branches: ["main"]   # main 푸시 시에만 실행
  workflow_dispatch:      # Actions 탭에서 수동 실행도 가능

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4

      - name: Generate index.html
        run: python3 scripts/generate_index.py

      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: "."
      - id: deployment
        uses: actions/deploy-pages@v4
```

### generate_index.py 기능

| 기능 | 동작 방식 |
|---|---|
| 파일 스캔 | 모든 폴더의 .html 파일을 재귀 탐색 (index.html, design-system.html 제외) |
| 메타데이터 추출 | `<title>`, `<meta name="description">`, `<meta property="og:image">`, 파일명 날짜 |
| 썸네일 처리 | og:image 있으면 이미지, 없으면 폴더별 그라디언트 + 제목 텍스트 |
| 버튼 주입 | 각 아티클에 "목록으로 돌아가기" 버튼 자동 삽입 (멱등성 보장) |
| 색상 변화 | 같은 폴더 내 카드도 4가지 그라디언트 변형을 순환 |

> `index.html`은 직접 편집하지 않는다. generate_index.py가 매 배포 시 덮어쓴다.  
> 목차 디자인을 바꾸려면 스크립트 안의 `build()` 함수를 수정한다.

---

## 파일 구성

```
my-html/
├── .claude/
│   └── commands/
│       └── html.md              ← /html 스킬 정의 (Claude Code 전용)
│
├── .github/
│   └── workflows/
│       └── deploy.yml           ← GitHub Actions 워크플로
│
├── scripts/
│   └── generate_index.py        ← 목차·버튼 자동 생성 스크립트
│
├── articles/                    ← 아티클 HTML (날짜-슬러그.html)
├── specs/                       ← 명세서
├── reviews/                     ← 코드 리뷰 문서
├── explore/                     ← 옵션 비교 문서
├── tools/                       ← 인터랙티브 도구
│
├── design-system.html           ← 디자인 규칙 참조 파일
└── index.html                   ← 자동 생성 (직접 편집 ✗)
```

| 파일 | 역할 | 편집 주체 |
|---|---|---|
| `html.md` | /html 스킬 — 아티클 작성 규칙 | 필요 시 수동 수정 |
| `deploy.yml` | GitHub Actions 트리거·단계 정의 | 처음 한 번만 설정 |
| `generate_index.py` | 목차 생성 + 버튼 주입 | GitHub Actions가 실행 |
| `design-system.html` | 색상·폰트·간격 디자인 규칙 | 디자인 변경 시 |
| `articles/*.html` | 실제 글 파일 | AI(/html 스킬) 생성 |
| `index.html` | 목차 페이지 | 자동 생성 (직접 ✗) |

---

## 새 레포지토리에 설치하기

### 1단계 — 파일 배치

| 파일 | 배치 경로 |
|---|---|
| `deploy.yml` | `.github/workflows/deploy.yml` |
| `generate_index.py` | `scripts/generate_index.py` |
| `design-system.html` | `design-system.html` (루트) |
| `html.md` | `.claude/commands/html.md` |

### 2단계 — GitHub Pages 소스 설정

Settings → Pages → Source를 **GitHub Actions**로 변경한다.

### 3단계 — 배포 환경 브랜치 허용

Settings → Environments → github-pages에서 **main** 브랜치의 배포를 허용한다.  
이 설정이 없으면 `Branch "main" is not allowed to deploy` 오류가 발생한다.

> 2단계와 3단계는 레포당 한 번만 설정하면 된다.

### 4단계 — 첫 아티클 작성 및 배포

```
/html article 첫 번째 글 주제
```

결과를 확인하고 푸시하면 자동 배포 완료.

---

## 다른 AI 서비스에 이식하기

GitHub Actions 파이프라인은 AI와 무관하게 작동한다.  
어떤 도구로 HTML을 만들어도 `articles/`에 넣고 main에 푸시하면 배포된다.

### 파일별 이식성

| 파일 | 이식성 | 다른 AI에서 사용하는 방법 |
|---|---|---|
| `deploy.yml` | ✅ 완전 이식 가능 | 그대로 사용 |
| `generate_index.py` | ✅ 완전 이식 가능 | 그대로 사용 |
| `design-system.html` | ✅ 완전 이식 가능 | 디자인 참조로 첨부 |
| `html.md` | ⚙️ 변환 필요 | 내용을 시스템 프롬프트로 붙여넣기 |

### 서비스별 적용 방법

| 서비스 | html.md 적용 방법 |
|---|---|
| ChatGPT Custom GPT | Configure → Instructions에 html.md 내용 붙여넣기 |
| Cursor / Windsurf | `.cursorrules` 파일에 작성 규칙 추가 |
| Gemini / 기타 챗봇 | 대화 첫 메시지에 html.md를 시스템 프롬프트로 제공 |
| 직접 작성 | design-system.html의 CSS 변수를 복사해 동일한 디자인으로 작성 |

> AI가 바뀌어도 파이프라인은 그대로다.  
> `articles/`에 넣고 main에 푸시하는 행위만으로 목차 재생성과 배포가 자동 실행된다.

---

## 요약

> **/html 스킬로 아티클을 만들고, 검토 후 main에 푸시하면 GitHub Actions가 목차를 재생성하고 GitHub Pages에 자동 배포한다. 파이프라인은 AI 도구에 종속되지 않아 어떤 서비스로도 이식 가능하다.**

| 구성 요소 | 역할 | 핵심 파일 |
|---|---|---|
| /html 스킬 | AI 아티클 생성 규칙 | `.claude/commands/html.md` |
| GitHub Actions | 자동 빌드·배포 | `.github/workflows/deploy.yml` |
| 목차 생성기 | index.html 자동 재생성 | `scripts/generate_index.py` |
| 디자인 시스템 | 통일된 시각 디자인 | `design-system.html` |
