<div align="center">
<img src="https://github.com/xorbitsai/inference/blob/043b673dbd93f1cd5c8d6b0bb481f8d605cd24d2/assets/xorbits-logo.png" width="180px" alt="xorbits" />

# Xorbits Inference Enterprise Documentation

<p align="center">
  <a href="./README.md"><img alt="README in English" src="https://img.shields.io/badge/English-454545?style=for-the-badge"></a>
  <a href="./README_zh_CN.md"><img alt="简体中文版自述文件" src="https://img.shields.io/badge/中文介绍-d9d9d9?style=for-the-badge"></a>
</p>

[![Deploy Documentation](https://github.com/xorbitsai/enterprise-docs/actions/workflows/deploy-docs.yml/badge.svg)](https://github.com/xorbitsai/enterprise-docs/actions/workflows/deploy-docs.yml)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://xorbitsai.github.io/enterprise-docs/)

</div>
<br />

## 📚 Online Documentation

- **English (default)**: [https://xorbitsai.github.io/enterprise-docs/](https://xorbitsai.github.io/enterprise-docs/)
- **简体中文**: [https://xorbitsai.github.io/enterprise-docs/zh-cn/](https://xorbitsai.github.io/enterprise-docs/zh-cn/)

The language menu matches the Xinference documentation: English, Simplified Chinese,
Traditional Chinese, Japanese, Korean, German, French, Spanish, Italian, and
Portuguese (Brazil). Existing `/en/` links redirect to the English pages at the root.

## 🚀 Features

This repository contains comprehensive documentation for Xorbits Inference Enterprise, including:

- **Multi-platform Support**: NVIDIA, Ascend/MindIE, Hygon and MetaX hardware platforms
- **Deployment Guides**: Single-node, multi-node, high availability and Prefill–Decode disaggregation
- **Enterprise Features**: License management, performance monitoring, troubleshooting
- **Multilingual**: Ten language editions with English as the default. Translation
  catalogs include machine-translated prose; commands and configuration literals
  are preserved. Translations can be reviewed in `docs/source/locale/`.
- **Interactive**: Live examples and configuration templates

The site organizes guides into getting started, hardware, models and performance,
clusters and availability, observability, and troubleshooting. Existing image-guide
URLs remain valid. Recorded cases state their environment, evidence and limitations;
missing version information is shown explicitly rather than inferred.

The visual layer extends PyData Sphinx Theme in `docs/source/_static/enterprise.css`.
Search, language menus, mobile navigation and theme switching use the theme's native
components. Imported PD screenshots live in `docs/source/_static/images/`.
Chinese search uses jieba and a small accelerator-name dictionary, following the
[Sphinx search configuration](https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-html_search_options).

Internal image-build and production AMI runbooks are not part of this public site.
