# AGENTS.md — coding-viewer

Guidance for coding agents (Codex and others) working in this repository.

## What this is

A small, dependency-free tool that shows the text codings of a QualCoder project as one web page.

- `index.html`: the viewer. Works standalone (loads `data.qda` in the browser with sql.js from cdnjs, or a JSON data file) or with data embedded at the `/*DATA*/null` marker.
- `build_viewer.py`: reads a QualCoder project **read-only** and writes either a self-contained HTML (`-o out.html`) or a data JSON (`--json -o out.json`). Standard library only, Python 3.9+.
- `examples/make_demo_project.py`: regenerates `examples/demo.qda/data.qda`, a tiny fictional project for testing.

## How to run for a user

When a user asks to "see/browse my QualCoder codings as a web page":

1. Ask for (or find) the project folder `*.qda` (it contains `data.qda`). Prefer that QualCoder is closed.
2. Run `python3 build_viewer.py <project.qda> -o <somewhere outside this repo>/coding-viewer.html`.
3. Optionally pass `--grades <judgements.json>` (exported from the page) to carry over earlier judgements.
4. Tell the user the output file contains raw transcript text and must not be shared or committed.

## Rules

- Never write to a QualCoder database. Always open it with `mode=ro`.
- Never commit real project files, generated HTML/JSON, or exported judgement files. `.gitignore` blocks `*.qda` (except `examples/demo.qda`), `coding-viewer*.html`, and `판단_*.json`; keep it that way.
- Keep `index.html` working without a build step and without any server. External scripts only from cdnjs with a pinned version.
- The data format shared by `build_viewer.py` and `index.html` must stay identical: `{title, generated, docs[{id,name}], cats[], codes[{cid,name,cat,color}], segs[{k,doc,pos,time,quote,before,after,memos[],codes[]}], grades{}}`, with segment key `k = "<document name>|<pos0>|<pos1>"`. If you change one side, change the other.
- The Reset button must clear every `localStorage` key starting with `cv-` and return to the load screen.

## Test

```bash
python3 examples/make_demo_project.py
python3 build_viewer.py examples/demo.qda -o /tmp/demo.html      # expect 2 docs, 7 codes, 9 segments, 10 codings
python3 build_viewer.py examples/demo.qda --json -o /tmp/demo.json
```

Then open `index.html`, load `examples/demo.qda/data.qda`, and check filtering, judgements, export/import and Reset.
