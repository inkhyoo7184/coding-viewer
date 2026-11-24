#!/usr/bin/env python3
"""시험용 가짜 QualCoder 프로젝트(examples/demo.qda/data.qda)를 만든다.

실제 자료가 아니다. 지어낸 짧은 면담 두 편(취미로 빵 굽기를 배운 이야기)과
코드 몇 개, 코딩 몇 개만 들어 있다. QualCoder 표 가운데 이 도구가 읽는
source, code_cat, code_name, code_text만 만든다.

  python3 examples/make_demo_project.py
  python3 build_viewer.py examples/demo.qda -o demo_viewer.html
"""
import shutil
import sqlite3
import tempfile
from pathlib import Path

OUT = Path(__file__).resolve().parent / "demo.qda"

DOCS = {
    1: ("가상 면담 1", "면담자 00:10 빵 굽기는 어떻게 시작하셨어요?\n\n참여자 00:25 처음에는 유튜브를 보고 따라 했어요. 영어 영상이 많아서 자막을 켜고 봤어요.\n\n"
                      "참여자 01:40 실패를 많이 했는데, 동네 빵집 사장님이 반죽 온도를 알려 주셔서 그때부터 잘됐어요.\n\n"
                      "면담자 02:10 지금은 어떠세요?\n\n참여자 02:30 이제는 친구들에게 가르쳐 주기도 해요. 제가 틀렸던 부분을 먼저 말해 줘요."),
    2: ("가상 면담 2", "면담자 00:05 요즘 어떻게 지내세요?\n\n참여자 00:20 주말마다 빵을 구워요. 레시피는 일본어 책을 번역기로 읽어요.\n\n"
                      "참여자 01:15 처음에는 계량이 너무 어려웠어요. 컵과 그램이 섞여 있어서요.\n\n"
                      "참여자 02:40 언젠가 작은 수업을 열고 싶어요. 그런데 아직 자신은 없어요."),
}
CATS = [(1, "배움의 경로", None), (2, "자원", None), (3, "도구", 2), (4, "앞으로", None)]
CODES = [  # cid, name, catid, supercid
    (1, "혼자 배우기", 1, None), (2, "다른 사람에게 배우기", 1, None),
    (3, "외국어 자료", 3, None), (4, "번역기", 3, 3),
    (5, "어려움", 1, None), (6, "가르치기", 4, None), (7, "자신감", 4, None),
]
CODINGS = [  # cid, fid, quote, memo
    (1, 1, "처음에는 유튜브를 보고 따라 했어요.", "[00:25] 혼자 시작함"),
    (3, 1, "영어 영상이 많아서 자막을 켜고 봤어요.", "[00:25]"),
    (2, 1, "동네 빵집 사장님이 반죽 온도를 알려 주셔서 그때부터 잘됐어요.", "[01:40] 바뀐 계기"),
    (5, 1, "실패를 많이 했는데,", "[01:40]"),
    (6, 1, "이제는 친구들에게 가르쳐 주기도 해요.", "[02:30] 확인 필요: 언제부터인지"),
    (3, 2, "레시피는 일본어 책을 번역기로 읽어요.", "[00:20]"),
    (4, 2, "레시피는 일본어 책을 번역기로 읽어요.", "[00:20]"),
    (5, 2, "처음에는 계량이 너무 어려웠어요.", "[01:15]"),
    (6, 2, "언젠가 작은 수업을 열고 싶어요.", "[02:40]"),
    (7, 2, "그런데 아직 자신은 없어요.", "[02:40] 긴장: 하고 싶음과 자신 없음"),
]


def main():
    OUT.mkdir(exist_ok=True)
    final = OUT / "data.qda"
    # 일부 외장 디스크(exFAT)에서는 새 SQLite 파일을 바로 만들면 실패하므로 임시 폴더에서 만든 뒤 복사한다.
    tmpdir = Path(tempfile.mkdtemp())
    db = tmpdir / "data.qda"
    con = sqlite3.connect(db)
    con.executescript("""
    create table source (id integer primary key, name text, fulltext text, mediapath text, memo text, owner text, date text, av_text_id integer, risid integer, unique(name));
    create table code_cat (catid integer primary key, name text, owner text, date text, memo text, supercatid integer, unique(name));
    create table code_name (cid integer primary key, name text, memo text, catid integer, owner text, date text, color text, supercid integer, unique(name));
    create table code_text (ctid integer primary key, cid integer, fid integer, seltext text, pos0 integer, pos1 integer, owner text, date text, memo text, avid integer, important integer, unique(cid,fid,pos0,pos1,owner));
    """)
    for fid, (name, text) in DOCS.items():
        con.execute("insert into source (id, name, fulltext, owner) values (?,?,?, 'demo')", (fid, name, text))
    con.executemany("insert into code_cat (catid, name, supercatid, owner) values (?,?,?, 'demo')", CATS)
    con.executemany("insert into code_name (cid, name, catid, supercid, owner) values (?,?,?,?, 'demo')", CODES)
    for cid, fid, quote, memo in CODINGS:
        p0 = DOCS[fid][1].index(quote)
        con.execute("insert into code_text (cid, fid, seltext, pos0, pos1, owner, memo) values (?,?,?,?,?, 'demo', ?)",
                    (cid, fid, quote, p0, p0 + len(quote), memo))
    con.commit()
    con.close()
    shutil.copyfile(db, final)
    shutil.rmtree(tmpdir, ignore_errors=True)
    print(f"가짜 프로젝트를 만들었습니다: {final}")


if __name__ == "__main__":
    main()
