# CLAUDE.md — 이 저장소 작업 지침

## 배포 흐름

```
article HTML 작성 → git add → git commit → git push origin main
                                              ↓
                                    GitHub Actions 자동 실행
                                    - generate_index.py 실행
                                    - 인덱스 재생성 커밋 [skip ci]
                                    - GitHub Pages 배포
```

## 절대 하지 말 것

- `python3 scripts/generate_index.py` 수동 실행 금지
- `index.html`, `vibe/index.html`, `insights/index.html`, `sw.js` 직접 수정 금지
- 위 파일들은 GitHub Actions가 단독으로 관리함

## 아티클 추가 절차

1. `vibe/` 또는 `insights/` 폴더에 HTML 파일 작성
2. `git add <파일>` — 아티클 파일만 스테이징
3. `git commit` 후 `git push origin main`
4. GitHub Actions가 인덱스 재생성 및 배포까지 자동 처리

## 브랜치 규칙

- 개발 브랜치에서 작업 후 `main`에 병합
- 병합 후 `git push origin main` → 자동 배포 트리거
