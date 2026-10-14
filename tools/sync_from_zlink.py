"""zlink(docs.zlink.systems)의 정본을 키트로 가져온다.

정본은 zlink 저장소에 있고 키트는 그것을 나르기만 한다. zlink 쪽 모양이 바뀌면 이 스크립트를
돌려 차이를 보고, 키트 버전을 올린다.

    python tools/sync_from_zlink.py D:/project/zlink          # 차이만 보인다
    python tools/sync_from_zlink.py D:/project/zlink --write  # 가져오고 SOURCE.md를 갱신한다

base.css와 헤더·메뉴 조각은 zlink 파일에서 ZLink 전용 부분을 뺀 것이라 그대로 덮지 않는다.
차이만 보이니 손으로 반영한다.
"""

from __future__ import annotations

import difflib
import subprocess
import sys
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
PKG = KIT / "crownchips_mkdocs_kit"

# (zlink 경로, 키트 경로, 그대로 복사하는가)
FILES = [
    ("framework/doc/framework/assets/korean.css", PKG / "assets/korean.css", True),
    ("doc/site/docs/assets/stylesheets/extra.css", PKG / "assets/base.css", False),
    ("doc/site/overrides/partials/header.html", PKG / "overrides/partials/header.html", False),
    ("doc/site/overrides/partials/nav.html", PKG / "overrides/partials/nav.html", False),
    ("doc/site/hooks/mermaid_size.py", PKG / "mermaid_size.py", True),
    ("doc/site/mkdocs.yml", None, False),
]


def commit_of(zlink: Path, rel: str) -> str:
    out = subprocess.run(["git", "-C", str(zlink), "log", "-1", "--format=%h %cs", "--", rel],
                         capture_output=True, text=True, check=True)
    return out.stdout.strip()


def main() -> None:
    zlink = Path(sys.argv[1])
    write = "--write" in sys.argv
    rows = []
    for rel, dest, copy in FILES:
        src = zlink / rel
        rows.append(f"| `{rel}` | {commit_of(zlink, rel)} | {'그대로' if copy else '공용 부분만(손으로 반영)'} |")
        if dest is None:
            print(f"[확인] {rel}: theme·features·markdown_extensions를 plugin.py와 눈으로 대조한다")
            continue
        a = dest.read_text(encoding="utf-8").splitlines()
        b = src.read_text(encoding="utf-8").splitlines()
        diff = list(difflib.unified_diff(a, b, f"kit/{dest.name}", f"zlink/{rel}", lineterm="", n=1))
        if not diff:
            print(f"[같음] {rel}")
        elif copy and write:
            dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8", newline="\n")
            print(f"[가져옴] {rel}")
        else:
            print(f"[다름] {rel} ({len(diff)}줄)")
            print("\n".join(diff[:60]))
    if write:
        (KIT / "SOURCE.md").write_text(
            "# 정본 출처\n\n키트의 모양은 docs.zlink.systems에서 가져온다. 아래 커밋 기준이다"
            "(`tools/sync_from_zlink.py`가 갱신한다).\n\n| zlink 파일 | 마지막 커밋 | 키트에서 |\n| --- | --- | --- |\n"
            + "\n".join(rows) + "\n", encoding="utf-8", newline="\n")
        print("SOURCE.md 갱신")


if __name__ == "__main__":
    main()
