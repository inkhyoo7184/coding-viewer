# CLAUDE.md — coding-viewer

이 저장소의 작업 규칙은 `AGENTS.md`에 있다. 먼저 그것을 읽는다.

요약:

- QualCoder 프로젝트는 읽기 전용으로만 연다.
- 사용자가 "코딩을 웹페이지로 보여 줘" 같은 부탁을 하면 `build_viewer.py`로 HTML을 **저장소 밖**에 만들고, 그 파일에 원문이 들어 있다는 점을 알린다.
- 실제 자료, 만든 HTML·JSON, 판단 파일은 커밋하지 않는다.
- `index.html`과 `build_viewer.py`의 데이터 형식은 함께 고친다.
- 같은 내용의 스킬은 `.claude/skills/coding-viewer/SKILL.md`에 있다. 다른 폴더에서도 쓰려면 `~/.claude/skills/`로 복사한다.
