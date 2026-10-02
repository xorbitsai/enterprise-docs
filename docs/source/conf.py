# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from i18n import docs_base_path, language_slug, sphinx_locale, switcher_config
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = 'Xinference'
copyright = '2023, Xorbits Inc.'
author = 'xorbitsai'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx_tabs.tabs",
    "sphinx_design",
    "IPython.sphinxext.ipython_directive",
    "IPython.sphinxext.ipython_console_highlighting",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build/**']

# i18n
locale_dirs = ["locale/"]  # path is example but recommended.
gettext_compact = False  # optional

# Language settings
language = sphinx_locale(language_slug(os.environ.get(
    'SPHINX_LANGUAGE', os.environ.get('READTHEDOCS_LANGUAGE', 'en'))))


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'pydata_sphinx_theme'
html_title = "Xinference"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
html_css_files = ['enterprise.css']
html_sidebars = {'**': ['enterprise-nav']}
if language.startswith('zh'):
    # Sphinx's Chinese index needs jieba and a dictionary for accelerator names.
    html_search_options = {'dict': str(Path(__file__).with_name('search-zh.txt'))}

# Define the version for our local documentation
version_match = language_slug(language)
json_url = docs_base_path() + "_static/switcher.json"

html_theme_options = {
    "show_toc_level": 2,
    "header_links_before_dropdown": 7,
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/xorbitsai/inference",
            "icon": "fa-brands fa-github",
            "type": "fontawesome",
        },
    ],
    "navbar_align": "content",  # [left, content, right] For testing that the navbar items align properly
    "navbar_start": ["enterprise-logo", "version-switcher"],
    "navbar_center": [],
    "navbar_end": [],
    "navbar_persistent": ["search-button-field", "theme-switcher"],
    "navigation_depth": 2,
    "show_nav_level": 1,
    "collapse_navigation": True,
    "show_prev_next": True,
    "secondary_sidebar_items": ["page-toc"],
    "switcher": {
        "json_url": json_url,
        "version_match": version_match,
    },
}


html_favicon = "_static/favicon.svg"


def apply_language_options(app, config):
    # Honor `sphinx-build -D language=...` as well as environment selection.
    slug = language_slug(config.language or 'en')
    options = config.html_theme_options
    options['switcher']['version_match'] = slug
    options['header_dropdown_text'] = {
        'en': 'More', 'zh-cn': '更多', 'zh-tw': '更多', 'ja': 'その他',
        'ko': '더보기', 'de': 'Mehr', 'fr': 'Plus', 'es': 'Más',
        'it': 'Altro', 'pt-br': 'Mais',
    }[slug]
    if slug in ('zh-cn', 'zh-tw'):
        options['icon_links'].extend([
            {'name': 'WeChat', 'url': 'https://xorbits.cn/assets/images/wechat_work_qr.png',
             'icon': 'fa-brands fa-weixin', 'type': 'fontawesome'},
            {'name': 'Zhihu', 'url': 'https://zhihu.com/org/xorbits',
             'icon': 'fa-brands fa-zhihu', 'type': 'fontawesome'},
        ])
        options['external_links'] = [
            {'name': '产品官网' if slug == 'zh-cn' else '產品官網', 'url': 'https://xorbits.cn'},
        ]
    else:
        options['icon_links'].extend([
            {'name': 'Discord', 'url': 'https://discord.gg/Xw9tszSkr5',
             'icon': 'fa-brands fa-discord', 'type': 'fontawesome'},
            {'name': 'Twitter', 'url': 'https://twitter.com/xorbitsio',
             'icon': 'fa-brands fa-twitter', 'type': 'fontawesome'},
        ])


def setup(app):
    app.connect('config-inited', apply_language_options)
    app.connect('build-finished', write_switcher_config)


def write_switcher_config(app, exception):
    if exception is None and app.builder.format == 'html':
        import json
        path = Path(app.outdir) / '_static/switcher.json'
        path.write_text(json.dumps(switcher_config(), ensure_ascii=False, indent=2) + '\n',
                        encoding='utf-8')
