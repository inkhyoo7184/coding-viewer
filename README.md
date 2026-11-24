# 코딩 한눈에 보기 (coding-viewer)

[QualCoder](https://github.com/ccbogel/QualCoder) 프로젝트에 붙인 코딩을 **구간별로 모아 웹페이지 한 장에서 살펴보는** 도구입니다. 코드를 눌러 거르고, 문서·검색어로 좁히고, 구간마다 앞뒤 문맥과 메모를 보고, 판단(예: 핵심/보조/보류/제외)과 메모를 남길 수 있습니다.

- **읽기 전용:** QualCoder 프로젝트 파일을 고치지 않습니다.
- **내 컴퓨터 안에서만:** 화면은 브라우저 안에서 파일을 읽습니다. 자료를 어디에도 올리지 않습니다.
- **Reset 버튼:** 오른쪽 위 Reset을 누르면 이 브라우저에 남은 판단·설정·화면 상태를 모두 지우고 처음 화면으로 돌아갑니다.

> 코드별 수는 참고용입니다. 질적 연구에서 코드 빈도를 결과로 쓸지는 연구 설계에 따라 정하세요.

**바로 쓰기:** https://inkhyoo7184.github.io/coding-viewer/
이 주소에 올라가 있는 것은 자료가 없는 빈 화면입니다. 여기서 고른 파일도 각자의 브라우저 안에서만 읽습니다.

## 세 가지 쓰는 법

### 1. 브라우저에서 바로 열기 (설치 없음)

1. 위 주소로 들어가거나, 내려받은 `index.html`을 브라우저로 엽니다(더블클릭).
2. **QualCoder 프로젝트 파일 열기**를 누르고, 프로젝트 폴더(예: `내프로젝트.qda`) 안의 `data.qda`를 고릅니다.
   - QualCoder는 닫아 두는 것이 좋습니다.
   - 이때 SQLite 해석기(sql.js)를 cdnjs에서 처음 한 번 받습니다. 자료는 밖으로 나가지 않습니다.
3. 바로 써 보려면 `examples/demo.qda/data.qda`(지어낸 시험용 자료)를 고르세요.

### 2. 데이터가 들어간 HTML 한 장 만들기 (인터넷 없이)

```bash
python3 build_viewer.py 내프로젝트.qda -o 코딩보기.html
```

Python 3.9 이상이면 되고, 따로 설치할 패키지는 없습니다. 만든 HTML에는 원문이 들어 있으니 **공유하거나 공개 저장소에 올리지 마세요.**

### 3. 데이터 JSON만 만들어 `index.html`에서 불러오기

```bash
python3 build_viewer.py 내프로젝트.qda --json -o 코딩데이터.json
```

`index.html`에서 **데이터 파일 열기 (JSON)**를 누르고 이 파일을 고릅니다.

## 판단 남기기

- 구간마다 판단 단계 단추와 판단 메모 칸이 있습니다. 판단은 이 브라우저에 저장됩니다.
- **판단 저장(파일)**로 JSON을 내려받아 두면 다른 컴퓨터나 다시 만든 화면에서 **판단 불러오기**로 이어 쓸 수 있습니다.
- HTML을 다시 만들 때 판단을 넣으려면 다음처럼 합니다.
  ```bash
  python3 build_viewer.py 내프로젝트.qda -o 코딩보기.html --grades 판단_내프로젝트_2026-01-01.json
  ```
- 판단은 `문서 이름|시작 위치|끝 위치`로 구간을 찾습니다. 코딩 위치가 바뀐 구간의 판단은 건너뛰고 알려 줍니다.
- **설정**에서 판단 단계(기본: 핵심, 보조, 보류, 제외)와 바로가기 검색어를 바꿀 수 있습니다. 메모에 바로가기 검색어가 들어 있으면 메모가 강조됩니다.

## 메모의 시각 표시

코딩 메모가 `[12:34]`처럼 대괄호 안의 시각으로 시작하면, 그 시각을 구간 옆에 따로 보여 줍니다.

## 파일

| 파일 | 하는 일 |
|---|---|
| `index.html` | 화면. 브라우저에서 바로 열거나, `build_viewer.py`가 데이터를 넣는 틀로 씁니다 |
| `build_viewer.py` | QualCoder 프로젝트(읽기 전용) → 데이터가 들어간 HTML 또는 JSON |
| `examples/make_demo_project.py` | 시험용 가짜 프로젝트(`examples/demo.qda`)를 다시 만듭니다 |
| `AGENTS.md` | Codex 같은 코딩 에이전트용 안내 |
| `CLAUDE.md`, `.claude/skills/coding-viewer/SKILL.md` | Claude Code용 안내와 스킬 |

## AI 코딩 도우미와 함께 쓰기

- **Claude Code:** 이 폴더에서 Claude Code를 열면 `CLAUDE.md`를 읽습니다. `.claude/skills/coding-viewer/`를 `~/.claude/skills/`에 복사하면 다른 폴더에서도 "QualCoder 코딩을 웹페이지로 보여 줘"라고 부탁할 수 있습니다.
- **Codex:** 이 폴더에서 Codex를 열면 `AGENTS.md`를 읽습니다.
- 어느 쪽이든 만든 HTML·JSON과 실제 프로젝트 파일을 저장소에 커밋하지 않도록 `.gitignore`가 막아 둡니다.

## 확인한 환경

QualCoder 3.x~4.x 프로젝트 형식(`source`, `code_cat`, `code_name`, `code_text` 표)에서 텍스트 코딩을 읽습니다. 이미지·음성·영상 코딩은 아직 읽지 않습니다.

---

## English (short)

**coding-viewer** turns the text codings of a [QualCoder](https://github.com/ccbogel/QualCoder) project into a single browsable web page: filter by code (AND), document, or keyword; see context and memos; and record your own judgements per segment.

- Try it at https://inkhyoo7184.github.io/coding-viewer/ (an empty page; your file is read only inside your browser).
- Open `index.html` and choose your project's `data.qda` (read in the browser via sql.js; nothing is uploaded), or
- `python3 build_viewer.py my.qda -o viewer.html` for a self-contained offline page, or `--json` for a data file.
- The **Reset** button (top right) clears everything this page stored in your browser.
- Generated files contain your raw data — do not publish them.

## License

MIT
