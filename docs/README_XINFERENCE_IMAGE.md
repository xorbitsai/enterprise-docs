# Xinference 镜像使用文档

本文档是从 `Xinference 镜像使用.docx` 转换而来的 Sphinx 格式文档。

## 文档内容

该文档包含了以下内容：

- **Nvidia系列**：CUDA环境下的Xinference镜像使用指南
- **MindIE系列**：华为昇腾NPU环境下的使用说明
- **海光系列**：海光DCU环境下的部署方法
- **证书更新**：Xinf企业版证书管理
- **性能测试**：benchmark测试工具使用
- **多机部署**：Supervisor和Worker集群部署配置
- **链路日志**：基于Langfuse的调用链路追踪和监控
- **K8s部署**：Kubernetes环境下的Helm部署配置

## 文件结构

```
docs/
├── source/
│   ├── xinference_images/          # 镜像使用文档目录
│   │   ├── index.rst               # 镜像使用总览页面
│   │   ├── nvidia.rst              # Nvidia系列镜像
│   │   ├── mindie.rst              # MindIE系列镜像
│   │   ├── hygon.rst               # 海光系列镜像
│   │   ├── license.rst             # 证书更新
│   │   ├── performance.rst         # 性能测试
│   │   ├── multi_deployment.rst    # 多机部署
│   │   ├── langfuse.rst            # 链路日志
│   │   └── kubernetes.rst          # K8s部署
│   ├── index.rst                   # 文档主索引
│   └── conf.py                     # Sphinx配置文件
├── build/html/                     # 生成的HTML文档
└── Makefile                        # 构建脚本
```

## 构建文档

### 1. 安装依赖

```bash
pip install sphinx sphinx-tabs sphinx-design pydata-sphinx-theme python-docx
```

### 2. 构建HTML文档

```bash
cd docs
make html
```

### 3. 查看文档

构建完成后，可以通过以下方式查看文档：

```bash
# 启动本地服务器
cd build/html
python -m http.server 8080
```

然后在浏览器中访问 `http://localhost:8080`

## 文档特性

- ✅ **模块化结构**：每个硬件平台独立页面，便于维护和查找
- ✅ **导航友好**：清晰的目录结构和页面间交叉引用
- ✅ 使用 reStructuredText 格式，符合 Sphinx 标准
- ✅ 包含完整的代码块高亮显示
- ✅ 支持多级目录结构和交叉引用
- ✅ 包含警告和注意事项的特殊标记
- ✅ 表格和列表格式化
- ✅ 响应式设计，支持移动端查看

## 原始文档信息

- 原始文件：`Xinference 镜像使用.docx`
- 转换时间：2025-09-25
- 转换工具：python-docx + 手工整理
- 文档格式：reStructuredText (.rst)

## 维护说明

如需更新文档内容：

1. 修改对应的 `.rst` 文件：
   - `source/xinference_images/nvidia.rst` - Nvidia系列
   - `source/xinference_images/mindie.rst` - MindIE系列
   - `source/xinference_images/hygon.rst` - 海光系列
   - `source/xinference_images/license.rst` - 证书管理
   - `source/xinference_images/performance.rst` - 性能测试
   - `source/xinference_images/multi_deployment.rst` - 多机部署
   - `source/xinference_images/langfuse.rst` - 链路日志
   - `source/xinference_images/kubernetes.rst` - K8s部署
2. 运行 `make html` 重新构建
3. 检查生成的HTML文档确保格式正确

## 注意事项

- 文档中包含的镜像拉取凭据仅为示例，实际使用时请使用正确的凭据
- K8s部署配置需要根据实际环境进行调整
- 性能测试结果会因硬件环境而异
