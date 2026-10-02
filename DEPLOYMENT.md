# GitHub Pages 部署指南

本文档说明如何将 Xorbits Inference Enterprise 文档部署到 GitHub Pages。

## 🚀 自动部署

### 前置条件

1. **GitHub 仓库设置**
   - 确保仓库是公开的（或者有 GitHub Pro/Team 账户用于私有仓库）
   - 在仓库设置中启用 GitHub Pages

2. **GitHub Pages 配置**
   - 进入仓库 Settings → Pages
   - Source 选择 "GitHub Actions"
   - 保存设置

### 部署流程

#### PR 构建验证
当你创建或更新 Pull Request 时，GitHub Actions 会自动：

1. **安装依赖**: 安装 Python 和 Sphinx 相关包
2. **构建文档**: 运行 `build_multilang.py` 生成 10 种语言的文档（默认英文）
3. **上传预览**: 将构建结果作为 artifacts 上传（保留7天）
4. **状态检查**: 在PR中显示构建状态和预览链接

#### 生产部署
当你推送代码到 `main` 或 `master` 分支时，GitHub Actions 会自动：

1. **构建文档**: 执行完整的多语言构建
2. **部署到 Pages**: 将构建结果发布到 GitHub Pages
3. **更新网站**: 实时更新在线文档

### 访问地址

部署完成后，文档将在以下地址可用：

- **英文文档（默认）**: `https://[username].github.io/[repository-name]/`
- **简体中文文档**: `https://[username].github.io/[repository-name]/zh-cn/`
- **其他语言**: `zh-tw/`、`ja/`、`ko/`、`de/`、`fr/`、`es/`、`it/`、`pt-br/`
- 旧的 `en/` 页面地址会跳转至根目录对应的英文页面。

例如：
- 英文: https://xorbitsai.github.io/enterprise-docs/
- 简体中文: https://xorbitsai.github.io/enterprise-docs/zh-cn/

## 🔧 手动部署

如果需要手动部署，可以按以下步骤操作：

### 1. 本地构建

```bash
cd docs
python build_multilang.py
```

### 2. 推送到 gh-pages 分支

```bash
# 安装 ghp-import（如果还没有安装）
pip install ghp-import

# 推送到 gh-pages 分支
ghp-import -n -p -f docs/build/html
```

## 📁 文件结构

```
enterprise-docs/
├── .github/
│   └── workflows/
│       └── deploy-docs.yml          # GitHub Actions 工作流
├── docs/
│   ├── source/
│   │   ├── .nojekyll               # 防止 Jekyll 处理
│   │   ├── conf.py                 # Sphinx 配置
│   │   └── ...                     # 文档源文件
│   ├── build_multilang.py          # 多语言构建脚本
│   ├── requirements.txt            # Python 依赖
│   └── build/
│       └── html/                   # 构建输出
│           ├── .nojekyll           # 复制到输出目录
│           ├── index.html          # 英文首页（默认）
│           └── zh-cn/              # 简体中文版本
│               └── index.html
├── README.md                       # 项目说明
└── DEPLOYMENT.md                   # 本文档
```

## 🛠️ 故障排除

### 常见问题

1. **构建失败**
   - 检查 `requirements.txt` 中的依赖版本
   - 查看 GitHub Actions 日志中的错误信息
   - 确认使用的是最新版本的 GitHub Actions

2. **页面显示异常**
   - 确保 `.nojekyll` 文件存在于输出目录
   - 检查相对路径是否正确

3. **多语言切换不工作**
   - 确认 `switcher.json` 文件已正确生成
   - 检查语言切换器配置

4. **GitHub Actions 版本错误**
   - 如果遇到 "deprecated version" 错误，确保使用最新版本：
     - `actions/setup-python@v5`
     - `actions/configure-pages@v4`
     - `actions/upload-pages-artifact@v3`
     - `actions/deploy-pages@v4`

### 调试步骤

1. **本地测试**
   ```bash
   cd docs
   python build_multilang.py --base-path /
   cd build/html
   python -m http.server 8080
   ```

2. **检查构建日志**
   - 在 GitHub 仓库的 Actions 标签页查看构建日志
   - 查找错误信息和警告

3. **验证文件**
   ```bash
   # 检查关键文件是否存在
   ls docs/build/html/.nojekyll
   ls docs/build/html/_static/switcher.json
   ls docs/build/html/zh-cn/_static/switcher.json
   ```

## 📝 自定义配置

### 修改域名

如果使用自定义域名，需要：

1. 在 `docs/source/` 目录下创建 `CNAME` 文件
2. 在文件中写入你的域名（如 `docs.example.com`）
3. 修改 `build_multilang.py` 复制 CNAME 文件到输出目录

### 修改基础路径

如果仓库名不是 `enterprise-docs`，需要：

1. 构建时设置 `DOCS_BASE_PATH=/[repository-name]/`，或使用 `python build_multilang.py --base-path /[repository-name]/`
2. 本地直接从网站根目录预览时使用 `--base-path /`。构建脚本会为所有语言生成正确的切换链接。

## 🔄 更新流程

1. **修改文档**: 编辑 `docs/source/` 下的 `.rst` 文件
2. **本地测试**: 运行 `python build_multilang.py` 验证构建
3. **提交推送**: 提交更改并推送到 main 分支
4. **自动部署**: GitHub Actions 自动构建和部署
5. **验证结果**: 访问 GitHub Pages 地址确认更新

## 📊 监控

- **构建状态**: 查看仓库 README 中的构建徽章
- **部署历史**: 在 GitHub Actions 页面查看部署历史
- **访问统计**: 在 GitHub Insights 中查看页面访问情况

## 多语言维护

语言列表与 inference 文档一致：英文、简体中文、繁体中文、日语、韩语、德语、法语、西班牙语、意大利语、葡萄牙语（巴西）。

- 语言名称、顺序和默认项统一维护在 `docs/source/_static/switcher.json`。
- URL 使用 `zh-cn`、`zh-tw`、`pt-br`；Sphinx 翻译目录分别为 `zh_CN`、`zh_TW`、`pt_BR`。
- 翻译保存在 `docs/source/locale/<locale>/LC_MESSAGES/*.po`。当前正文已补齐机器翻译，后续可在这些文件中校对；命令、参数、配置值和引用目标保持原样。
- 编辑原文后重新构建会更新翻译目录。新增或变化的条目需要补充译文；构建本身不调用在线翻译服务。
- CI 构建后运行 `python verify_multilang.py`，检查语言列表、页面、切换链接和旧英文地址兼容性。
