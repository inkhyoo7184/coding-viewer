#!/usr/bin/env python3
"""QualCoder 프로젝트의 코딩을 '코딩 한눈에 보기' 화면으로 만든다.

QualCoder 프로젝트(.qda 폴더 또는 그 안의 data.qda)를 읽기 전용으로 열어
코딩 구간을 모은 뒤, 데이터가 들어간 HTML 한 장이나 JSON 파일을 만든다.
프로젝트 파일은 고치지 않는다.

예:
  python3 build_viewer.py 내프로젝트.qda -o 코딩보기.html
  python3 build_viewer.py 내프로젝트.qda --json -o 코딩데이터.json
  python3 build_viewer.py 내프로젝트.qda -o 코딩보기.html --grades 판단_내프로젝트_2026-01-01.json

Build a "coding viewer" page from a QualCoder project (read-only).
"""
import argparse
import datetime as dt
import json
import re
import sqlite3
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIME_RE = re.compile(r"^\s*\[([0-9:–~\-]+)\]\s*")


def find_db(path: Path) -> Path:
    if path.is_dir():
        db = path / "data.qda"
        if not db.exists():
            sys.exit(f"data.qda를 찾지 못했습니다: {path}")
        return db
    if path.exists():
        return path
    sys.exit(f"파일이 없습니다: {path}")


def build(db_path: Path, title: str, context: int = 90) -> dict:
    con = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    tables = {r[0] for r in con.execute("select name from sqlite_master where type='table'")}
    for t in ("source", "code_cat", "code_name", "code_text"):
        if t not in tables:
            sys.exit(f"QualCoder 프로젝트가 아닌 것 같습니다({t} 표가 없음): {db_path}")

    cats = [dict(r) for r in con.execute("select catid, name, supercatid from code_cat")]
    cat_by_id = {c["catid"]: c for c in cats}

    def cat_path(catid):
        parts, c, guard = [], cat_by_id.get(catid), 0
        while c and guard < 20:
            parts.insert(0, c["name"])
            c = cat_by_id.get(c["supercatid"])
            guard += 1
        return " › ".join(parts) or "(범주 없음)"

    codes = [dict(r) for r in con.execute("select cid, name, catid, supercid, color from code_name")]
    code_by_id = {c["cid"]: c for c in codes}

    def code_name(c):
        parts, p, guard = [c["name"]], code_by_id.get(c["supercid"]), 0
        while p and guard < 20:
            parts.insert(0, p["name"])
            p = code_by_id.get(p["supercid"])
            guard += 1
        return " › ".join(parts)

    cat_names, out_codes = [], []
    for c in codes:
        cat = cat_path(c["catid"])
        if cat not in cat_names:
            cat_names.append(cat)
        out_codes.append({"cid": c["cid"], "name": code_name(c), "cat": cat, "color": c["color"] or ""})
    order = [cat_path(c["catid"]) for c in sorted(cats, key=lambda c: c["catid"])]
    order = [n for n in dict.fromkeys(order) if n in cat_names] + [n for n in cat_names if n not in order]
    out_codes.sort(key=lambda c: (order.index(c["cat"]), c["cid"]))

    text, docs = {}, []
    for r in con.execute("select id, name, fulltext from source where fulltext is not null order by id"):
        text[r["id"]] = r["fulltext"] or ""
        docs.append({"id": r["id"], "name": r["name"] or f"문서 {r['id']}"})
    doc_name = {d["id"]: d["name"] for d in docs}

    segs = {}
    for r in con.execute("select ctid, cid, fid, seltext, pos0, pos1, memo from code_text "
                         "order by fid, pos0, pos1, ctid"):
        if r["fid"] not in text:
            continue
        key = f"{doc_name[r['fid']]}|{r['pos0']}|{r['pos1']}"
        if key not in segs:
            t = text[r["fid"]]
            m = TIME_RE.match(r["memo"] or "")
            segs[key] = {
                "k": key, "doc": r["fid"], "pos": r["pos0"], "time": m.group(1) if m else "",
                "quote": r["seltext"] or t[r["pos0"]:r["pos1"]],
                "before": t[max(0, r["pos0"] - context):r["pos0"]],
                "after": t[r["pos1"]:r["pos1"] + context],
                "memos": [], "codes": [],
            }
        s = segs[key]
        memo = TIME_RE.sub("", r["memo"] or "").strip()
        if memo and memo not in s["memos"]:
            s["memos"].append(memo)
        if r["cid"] not in s["codes"]:
            s["codes"].append(r["cid"])
    con.close()
    return {"title": title, "generated": dt.datetime.now().isoformat(timespec="seconds"),
            "docs": docs, "cats": order, "codes": out_codes, "segs": list(segs.values()), "grades": {}}


def main():
    ap = argparse.ArgumentParser(description="QualCoder 코딩을 웹페이지로 모아 보기 (읽기 전용)")
    ap.add_argument("project", type=Path, help="QualCoder 프로젝트 폴더(.qda) 또는 그 안의 data.qda")
    ap.add_argument("-o", "--out", type=Path, required=True, help="만들 파일(.html 또는 --json이면 .json)")
    ap.add_argument("--json", action="store_true", help="HTML 대신 데이터 JSON만 만든다(index.html에서 불러오기용)")
    ap.add_argument("--title", help="화면 제목(기본: 프로젝트 이름)")
    ap.add_argument("--grades", type=Path, help="화면의 '판단 저장(파일)'로 받은 JSON. 판단을 함께 넣는다")
    ap.add_argument("--context", type=int, default=90, help="앞뒤 문맥 글자 수(기본 90)")
    ap.add_argument("--template", type=Path, default=HERE / "index.html", help="화면 틀(기본: index.html)")
    a = ap.parse_args()

    db = find_db(a.project)
    title = a.title or (a.project.name if a.project.is_dir() else a.project.parent.name).removesuffix(".qda")
    data = build(db, title, a.context)

    if a.grades:
        saved = json.loads(a.grades.read_text(encoding="utf-8")).get("grades", {})
        keys = {s["k"] for s in data["segs"]}
        data["grades"] = {k: v for k, v in saved.items() if k in keys}
        lost = [k for k in saved if k not in keys]
        print(f"판단 {len(data['grades'])}개를 넣었습니다." + (f" 맞는 구간이 없는 판단 {len(lost)}개는 건너뛰었습니다." if lost else ""))

    if a.json:
        a.out.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    else:
        html = a.template.read_text(encoding="utf-8")
        marker = "/*DATA*/null"
        if marker not in html:
            sys.exit("템플릿에서 데이터 자리(/*DATA*/null)를 찾지 못했습니다.")
        payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
        a.out.write_text(html.replace(marker, payload, 1), encoding="utf-8")
    n_cod = sum(len(s["codes"]) for s in data["segs"])
    print(f"{a.out}: 문서 {len(data['docs'])}개, 코드 {len(data['codes'])}개, 구간 {len(data['segs'])}개, 코딩 {n_cod}개")
    print("주의: 만든 파일에는 원문이 들어 있습니다. 공개 저장소에 올리지 마세요.")


if __name__ == "__main__":
    main()
