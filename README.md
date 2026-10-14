# crownchips-mkdocs-kit

crownchips 기획서 사이트들의 공용 모양이다. [docs.zlink.systems](https://docs.zlink.systems/)와 같은 글꼴·글자 크기·행간·간격·코드 블록·목차를 MkDocs Material에 준다. 모양을 바꿀 때는 이 저장소만 고치고 버전을 올린다.

| 사이트 | 저장소 |
| --- | --- |
| [docs.crownchips.com](https://docs.crownchips.com) (목록) | crownchips/docs-hub |
| cc-games.docs.crownchips.com | crownchips/cc-games |
| jpoker.docs.crownchips.com | crownchips/jpoker |
| casino.docs.crownchips.com | crownchips/crownchips |
| business.docs.crownchips.com | crownchips/business-plan |

## 쓰는 법

`docs/requirements.txt`:

```text
crownchips-mkdocs-kit @ git+https://github.com/crownchips/mkdocs-kit@v1.0.0
```

`mkdocs.yml`:

```yaml
site_name: 프로젝트 기획서
docs_dir: docs

plugins:
  - search
  - crownchips-kit

theme:
  name: material
  features:            # 이 사이트에만 더하는 기능(없으면 줄째 생략)
    - navigation.indexes

extra_css:
  - assets/extra.css   # 이 프로젝트에만 필요한 것(그림 격자 등)

nav:
  - 개요: index.md
```

로컬 미리보기:

```bash
pip install -r docs/requirements.txt
python -m mkdocs serve
```

## 키트가 정하는 것

| 항목 | 값 |
| --- | --- |
| 글꼴·크기·간격 | `assets/korean.css`(zlink 정본 그대로): 시스템 한글 글꼴, 본문 14px·행간 1.62, 제목 배율·굵기, 산문 폭 46rem, 표·코드 블록·인라인 코드, 좌측 목차 폭 |
| 탭·코드 보조 | `assets/base.css`(zlink extra.css의 공용 부분) |
| 테마 | 언어 ko, `font: false`, 팔레트 slate(먼저)·default, teal |
| 기능 | `content.code.copy`, `content.tabs.link`, `navigation.instant`(+progress), `navigation.top`, `navigation.footer`, `search.highlight` + 저장소가 더한 기능 |
| 마크다운 확장 | admonition, attr_list, md_in_html, tables, details, emoji, highlight, inlinehilite, superfences(mermaid), tabbed, tasklist, toc(목차 `##`까지, 한글 anchor) |
| 헤더·메뉴 | 사이트 이름 글자도 홈으로 링크 |
| mermaid | 글씨를 키우고 간격을 줄인다(`mermaid_size: false`로 끈다) |

저장소의 `extra_css`는 키트 CSS 뒤에 붙으므로 프로젝트별로 덮을 수 있다. 키트와 같은 값을 저장소에 다시 적지 않는다.

## zlink와 맞추기

정본은 zlink 저장소다. 출처 커밋은 [SOURCE.md](SOURCE.md)에 있다.

```bash
python tools/sync_from_zlink.py D:/project/zlink          # 차이 보기
python tools/sync_from_zlink.py D:/project/zlink --write  # korean.css·mermaid 가져오기 + SOURCE.md
```

가져온 뒤 `pyproject.toml`과 `__init__.py`의 버전을 올리고 태그(`v1.x.y`)를 단다. 각 저장소의 `docs/requirements.txt` 태그를 올리면 다음 배포부터 바뀐다.

## 새 프로젝트

crownchips/docs-hub의 `scripts/new-project.sh`가 mkdocs.yml·requirements·배포 workflow·Cloudflare Pages·주소·잠금·목록 카드를 한 번에 만든다.
