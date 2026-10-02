"""Language metadata shared by Sphinx and the multilingual builder."""

import json
import os
from pathlib import Path

LANGUAGES = json.loads(
    (Path(__file__).parent / "source/_static/switcher.json").read_text(encoding="utf-8")
)
LOCALES = {"zh-cn": "zh_CN", "zh-tw": "zh_TW", "pt-br": "pt_BR"}


def sphinx_locale(slug):
    return LOCALES.get(slug, slug)


def language_slug(locale):
    slug = locale.replace("_", "-").lower()
    if slug not in {item["version"] for item in LANGUAGES}:
        raise ValueError(f"Unsupported documentation language: {locale}")
    return slug


def docs_base_path(value=None):
    value = value if value is not None else os.environ.get("DOCS_BASE_PATH", "/enterprise-docs/")
    if not value or value == "/":
        return "/"
    return "/" + value.strip("/") + "/"


def switcher_config(base_path=None):
    base_path = docs_base_path(base_path)
    return [dict(item, url=base_path + ("" if item["version"] == "en" else item["version"] + "/"))
            for item in LANGUAGES]
