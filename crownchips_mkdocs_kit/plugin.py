"""crownchips-kit — 기획서 사이트의 모양을 한 곳에서 정한다.

docs.zlink.systems와 같은 모양(글꼴·글자 크기·행간·간격·코드 블록·목차)을 모든 기획서
저장소에 똑같이 준다. 저장소의 `mkdocs.yml`은 `theme: name: material`과 `plugins: [search,
crownchips-kit]`만 두고, 테마·팔레트·기능·마크다운 확장은 이 플러그인이 채운다.

저장소가 따로 정하는 것은 그 프로젝트에만 필요한 것뿐이다: 사이트 이름, nav, 그 프로젝트의
`extra_css`(그림 격자 등), 추가 기능(`navigation.indexes` 같은 것). 기능은 합쳐지고, 나머지
모양 값은 키트가 정한다.
"""

from __future__ import annotations

from pathlib import Path

from material.extensions.emoji import to_svg, twemoji
from mkdocs.config import config_options as c
from mkdocs.config.base import Config
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import File
from pymdownx.slugs import slugify
from pymdownx.superfences import fence_code_format

from . import mermaid_size

HERE = Path(__file__).parent

# 키트가 사이트에 올리는 CSS. 저장소의 extra_css보다 앞에 둬서 저장소가 덮을 수 있다.
KIT_CSS = ("korean.css", "base.css", "lightbox.css")
# 본문 그림 클릭 확대.
KIT_JS = ("lightbox.js",)
KIT_CSS_DIR = "assets/crownchips-kit"

PALETTE = [
    {"scheme": "slate", "primary": "teal", "accent": "teal",
     "toggle": {"icon": "material/weather-sunny", "name": "밝은 화면으로"}},
    {"scheme": "default", "primary": "teal", "accent": "teal",
     "toggle": {"icon": "material/weather-night", "name": "어두운 화면으로"}},
]

FEATURES = [
    "content.code.copy",
    "content.tabs.link",
    "navigation.instant",
    "navigation.instant.progress",
    "navigation.top",
    "navigation.footer",
    "search.highlight",
]

# docs.zlink.systems의 확장 목록에서 ZLink 전용(snippets의 저장소 경로)을 뺀 것.
EXTENSIONS: dict[str, dict] = {
    "admonition": {},
    "attr_list": {},
    "md_in_html": {},
    "tables": {},
    "pymdownx.details": {},
    "pymdownx.emoji": {"emoji_index": twemoji, "emoji_generator": to_svg},
    "pymdownx.highlight": {"anchor_linenums": True, "line_spans": "__span", "pygments_lang_class": True},
    "pymdownx.inlinehilite": {},
    "pymdownx.superfences": {"custom_fences": [
        {"name": "mermaid", "class": "mermaid", "format": fence_code_format}]},
    "pymdownx.tabbed": {"alternate_style": True},
    "pymdownx.tasklist": {"custom_checkbox": True},
    # 왼쪽 목차는 `##`까지. 한글 제목 anchor가 살아남도록 unicode slug.
    "toc": {"permalink": True, "toc_depth": 2, "slugify": slugify(case="lower", unicode=True)},
}


class KitConfig(Config):
    # mermaid 글씨 키우기(docs.zlink.systems와 같다). 문서가 %%{init}%%로 직접 정하면 건드리지 않는다.
    mermaid_size = c.Type(bool, default=True)


class KitPlugin(BasePlugin[KitConfig]):
    def on_config(self, config):
        theme = config.theme
        if theme.name != "material":
            raise PluginError("crownchips-kit은 theme: name: material 위에서만 쓴다.")

        theme["language"] = "ko"
        # Material 기본 Roboto에는 한글 글리프가 없다. 글꼴은 korean.css가 시스템 한글 글꼴로 정한다.
        theme["font"] = False
        theme["palette"] = PALETTE
        extra = [f for f in (theme.get("features") or []) if f not in FEATURES]
        theme["features"] = FEATURES + extra

        # 헤더·메뉴 조각(사이트 이름 텍스트도 홈 링크). 저장소의 custom_dir이 있으면 그 다음에 둔다.
        overrides = str(HERE / "overrides")
        if overrides not in theme.dirs:
            theme.dirs.insert(1 if theme.custom_dir else 0, overrides)

        for name, options in EXTENSIONS.items():
            if name not in config.markdown_extensions:
                config.markdown_extensions.append(name)
            if options:
                config.mdx_configs[name] = {**config.mdx_configs.get(name, {}), **options}

        kit_css = [f"{KIT_CSS_DIR}/{n}" for n in KIT_CSS]
        config.extra_css[:0] = [p for p in kit_css if p not in config.extra_css]
        for p in (f"{KIT_CSS_DIR}/{n}" for n in KIT_JS):
            if p not in config.extra_javascript:
                config.extra_javascript.append(p)
        return config

    def on_files(self, files, config):
        for name in KIT_CSS + KIT_JS:
            files.append(File.generated(config, f"{KIT_CSS_DIR}/{name}", abs_src_path=str(HERE / "assets" / name)))
        return files

    def on_page_markdown(self, markdown, **kwargs):
        if self.config.mermaid_size:
            return mermaid_size.on_page_markdown(markdown, **kwargs)
        return markdown
