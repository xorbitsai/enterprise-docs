#!/usr/bin/env python3
"""Build every documentation language, with English at the site root."""

import argparse
import html
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from i18n import LANGUAGES, docs_base_path, sphinx_locale, switcher_config

DOCS_DIR = Path(__file__).resolve().parent


def run_command(args, env=None):
    print(f"Running: {' '.join(map(str, args))}", flush=True)
    subprocess.run(args, cwd=DOCS_DIR, env=env, check=True)


def build_language(slug, output_dir, base_path, doctrees_dir):
    env = os.environ.copy()
    env.update(SPHINX_LANGUAGE=sphinx_locale(slug), DOCS_BASE_PATH=base_path)
    # Each language needs its own Sphinx environment and search index.
    run_command([
        sys.executable, "-m", "sphinx", "-b", "html", "-E", "-W", "--keep-going",
        "-d", str(doctrees_dir / slug),
        "-D", f"language={sphinx_locale(slug)}",
        "source", str(output_dir),
    ], env=env)


def write_english_redirects(output_dir, base_path):
    """Preserve previously published /en/ links, including nested pages."""
    for page in list(output_dir.rglob("*.html")):
        relative = page.relative_to(output_dir)
        target = html.escape(base_path + relative.as_posix(), quote=True)
        redirect = output_dir / "en" / relative
        redirect.parent.mkdir(parents=True, exist_ok=True)
        redirect.write_text(
            '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<link rel="canonical" href="{target}">'
            f'<meta http-equiv="refresh" content="0;url={target}">'
            f'<title>Redirecting</title></head><body><a href="{target}">'
            'Continue to the English documentation</a></body></html>\n',
            encoding="utf-8",
        )


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=DOCS_DIR / "build/html")
    parser.add_argument("--base-path", default=docs_base_path(),
                        help="Site URL prefix; use / for a local preview.")
    args = parser.parse_args(argv)
    output_dir = args.output_dir.resolve()
    base_path = docs_base_path(args.base_path)
    if (output_dir == Path(output_dir.anchor) or output_dir in DOCS_DIR.parents
            or output_dir == DOCS_DIR or output_dir == Path.cwd()
            or output_dir.is_relative_to(DOCS_DIR / "source")):
        parser.error("output directory must not contain documentation sources")
    try:
        run_command([sys.executable, "-m", "sphinx", "-b", "gettext", "-E", "-W", "--keep-going",
                     "source", "build/locale"])
        locales = [sphinx_locale(item["version"]) for item in LANGUAGES]
        run_command([sys.executable, "-m", "sphinx_intl", "update",
                     "-p", "build/locale", "-d", "source/locale",
                     *[arg for loc in locales for arg in ("-l", loc)]])
        run_command([sys.executable, "-m", "sphinx_intl", "build", "-d", "source/locale"])
        if output_dir.exists():
            shutil.rmtree(output_dir)
        doctrees_dir = output_dir.parent / f".{output_dir.name}-doctrees"
        build_language("en", output_dir, base_path, doctrees_dir)
        write_english_redirects(output_dir, base_path)
        for item in LANGUAGES:
            slug = item["version"]
            if slug != "en":
                build_language(slug, output_dir / slug, base_path, doctrees_dir)
        config = json.dumps(switcher_config(base_path), ensure_ascii=False, indent=2) + "\n"
        for item in LANGUAGES:
            directory = output_dir if item["version"] == "en" else output_dir / item["version"]
            (directory / "_static/switcher.json").write_text(config, encoding="utf-8")
        shutil.copy2(DOCS_DIR / "source/.nojekyll", output_dir / ".nojekyll")
    except subprocess.CalledProcessError as exc:
        print(f"Documentation build failed (exit {exc.returncode}).", file=sys.stderr)
        return 1
    print(f"Built {len(LANGUAGES)} languages in {output_dir}; default: English.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
