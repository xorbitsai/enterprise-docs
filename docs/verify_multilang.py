#!/usr/bin/env python3
"""Check published language routes, translated prose, and technical literals."""

import argparse
from collections import Counter
from html.parser import HTMLParser
import json
from pathlib import Path
import re

from babel.messages.pofile import read_po
from i18n import LANGUAGES, docs_base_path, sphinx_locale, switcher_config

DOCS_DIR = Path(__file__).resolve().parent
TASK_SECTIONS = ('getting_started', 'hardware', 'deployment', 'cluster',
                 'observability', 'troubleshooting')
LITERALS = re.compile(r':\w+:`[^`]*`|``[^`]*``|`[^`]*`_{0,2}|https?://\S+')


def literals(text):
    # A sentence's final punctuation is outside a bare URL in reStructuredText.
    return Counter(token.rstrip('.,;:，。；：') if token.startswith(('http://', 'https://'))
                   else token for token in LITERALS.findall(text))


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.language = None
        self.heading = ''
        self.in_heading = False
        self.code_blocks = []
        self.in_code = False
        self.problematic = False
        self.feed(path.read_text(encoding='utf-8'))

    def handle_starttag(self, tag, attrs):
        if 'problematic' in dict(attrs).get('class', '').split():
            self.problematic = True
        if tag == 'html':
            self.language = dict(attrs).get('lang', '').replace('_', '-').lower()
        if tag == 'h1':
            self.in_heading = True
        if tag == 'pre':
            self.in_code = True
            self.code_blocks.append('')

    def handle_endtag(self, tag):
        if tag == 'h1':
            self.in_heading = False
        if tag == 'pre':
            self.in_code = False

    def handle_data(self, data):
        if self.in_heading:
            self.heading += data
        if self.in_code:
            self.code_blocks[-1] += data


def check_catalogs():
    locale_root = DOCS_DIR / 'source/locale'
    expected = {p.relative_to(locale_root / 'en/LC_MESSAGES')
                for p in (locale_root / 'en/LC_MESSAGES').rglob('*.po')}
    for language in LANGUAGES:
        locale = sphinx_locale(language['version'])
        directory = locale_root / locale / 'LC_MESSAGES'
        assert {p.relative_to(directory) for p in directory.rglob('*.po')} == expected, locale
        for relative in expected:
            with (directory / relative).open('rb') as stream:
                catalog = read_po(stream, locale=locale)
            for message in catalog:
                if not message.id:
                    continue
                assert message.string and not message.fuzzy, f'{locale}/{relative}: missing translation'
                assert '▁' not in message.string, f'{locale}/{relative}: unprocessed tokenizer output'
                assert literals(message.id) == literals(message.string), \
                    f'{locale}/{relative}: changed technical literal or reference'
                assert message.id.count('**') == message.string.count('**'), \
                    f'{locale}/{relative}: changed emphasis markup'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, default=DOCS_DIR / 'build/html')
    parser.add_argument('--base-path', default=docs_base_path())
    args = parser.parse_args(argv)
    root = args.output_dir.resolve()
    base_path = docs_base_path(args.base_path)
    check_catalogs()
    expected = switcher_config(base_path)
    assert [item['version'] for item in expected if item.get('preferred')] == ['en']
    source_pages = {p.relative_to(DOCS_DIR / 'source').with_suffix('.html')
                    for p in (DOCS_DIR / 'source').rglob('*.rst')
                    if '_build' not in p.parts}
    for language in LANGUAGES:
        slug = language['version']
        directory = root if slug == 'en' else root / slug
        config = json.loads((directory / '_static/switcher.json').read_text())
        assert config == expected, f'{slug}: inconsistent switcher'
        home = (directory / 'index.html').read_text(encoding='utf-8')
        assert 'enterprise.css' in home, f'{slug}: missing enterprise theme'
        assert 'hide-on-wide' not in home.split('id="pst-primary-sidebar"')[1].split('>')[0], \
            f'{slug}: task navigation hidden on the home page'
        for section in TASK_SECTIONS:
            assert f'href="{section}/index.html"' in home, f'{slug}: missing task section {section}'
        for screenshot in ('pd-deploy-form.png', 'pd-role-dropdown.png'):
            assert (directory / '_static/images' / screenshot).is_file(), f'{slug}: missing PD screenshot'
        for internal in ('SAAS_IMAGE_BUILD.html', 'ami-bake-runbook.html'):
            assert not (directory / internal).exists(), f'{slug}: internal runbook published'
        for item in config:
            assert item['url'].startswith(base_path)
            target = root / item['url'][len(base_path):] / 'index.html'
            assert target.is_file(), f'{slug}: broken language URL'
        for relative in source_pages | {Path('search.html'), Path('genindex.html')}:
            path = directory / relative
            assert path.is_file(), f'{slug}: missing {relative}'
            page = Page(path)
            assert page.language == slug, f'{slug}/{relative}: incorrect HTML language {page.language}'
            assert not page.problematic, f'{slug}/{relative}: malformed reStructuredText'
            assert page.code_blocks == Page(root / relative).code_blocks, \
                f'{slug}/{relative}: changed command or configuration block'
            text = path.read_text(encoding='utf-8')
            assert re.search(r"theme_switcher_version_match\s*=\s*['\"]" + re.escape(slug) + r"['\"]", text), \
                f'{slug}/{relative}: incorrect selected language'
            assert base_path + '_static/switcher.json' in text, f'{slug}/{relative}: broken switcher path'
        for relative in (Path('xinference_images/index.html'), Path('xinference_images/nvidia.html')):
            title = Page(directory / relative).heading
            assert title.strip(), f'{slug}: missing translated heading'
            if slug not in ('zh-cn', 'zh-tw', 'ja'):
                assert not re.search('[\u4e00-\u9fff]', title), f'{slug}: untranslated heading'
        assert (directory / 'searchindex.js').is_file(), f'{slug}: missing search index'
        if slug in ('zh-cn', 'zh-tw'):
            index_text = (directory / 'searchindex.js').read_text(encoding='utf-8')
            index = json.loads(index_text.removeprefix('Search.setIndex(').removesuffix(')'))
            metax = index['docnames'].index('hardware/metax')
            term_docs = index['titleterms'].get('沐曦', [])
            if isinstance(term_docs, int):
                term_docs = [term_docs]
            assert metax in term_docs, f'{slug}: Chinese search cannot find the MetaX guide'
    for relative in source_pages | {Path('search.html'), Path('genindex.html')}:
        redirect = (root / 'en' / relative).read_text(encoding='utf-8')
        assert f'content="0;url={base_path}{relative.as_posix()}"' in redirect
    assert (root / '.nojekyll').is_file()
    print(f'Checked {len(LANGUAGES)} languages: catalogs, literals, pages, switchers, and English redirects.')


if __name__ == '__main__':
    main()
