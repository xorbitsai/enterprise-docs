#!/usr/bin/env python3
"""
批量填写关键英文翻译
"""

import os
import re
from pathlib import Path

# 关键术语翻译映射
TRANSLATIONS = {
    # 主要标题和概念
    "Xinference 镜像使用": "Xinference Image Usage",
    "概述": "Overview", 
    "目录": "Contents",
    "使用说明": "Usage Instructions",
    "版本信息": "Version Information",
    "依赖": "Dependencies",
    "拉取镜像": "Pull Image",
    "启动指令示例": "Startup Command Examples",
    "启动Xinference": "Start Xinference",
    "相关文档": "Related Documentation",
    
    # 硬件平台
    "Nvidia系列": "NVIDIA Series",
    "MindIE系列": "MindIE Series", 
    "海光系列": "Hygon Series",
    "适用于CUDA环境的GPU加速推理": "GPU-accelerated inference for CUDA environments",
    "适用于华为昇腾NPU环境": "For Huawei Ascend NPU environments",
    "适用于海光DCU环境": "For Hygon DCU environments",
    
    # 功能模块
    "证书更新": "License Updates",
    "性能测试": "Performance Testing", 
    "多机部署": "Multi-Machine Deployment",
    "链路日志": "Chain Logging",
    "企业版链路日志使用": "Enterprise Chain Logging Usage",
    "管理和配置": "Management and Configuration",
    "硬件平台": "Hardware Platforms",
    
    # 部署相关
    "在 K8s 上部署": "Deploy on K8s",
    "Xinference 多机部署": "Xinference Multi-Machine Deployment",
    "启动Supervisor": "Start Supervisor",
    "启动Worker": "Start Worker",
    "部署验证": "Deployment Verification",
    
    # 监控相关
    "模型调用": "Model Invocation",
    "链路状态": "Chain Status", 
    "链路详情": "Chain Details",
    "性能指标": "Performance Metrics",
    "调用统计": "Invocation Statistics",
    
    # 常用词汇
    "选择指南": "Selection Guide",
    "常见任务": "Common Tasks", 
    "支持与帮助": "Support and Help",
    "故障排除": "Troubleshooting",
    "配置文件": "Configuration Files",
    "注意事项": "Notes",
    "示例": "Example",
    "参数说明": "Parameter Description",
    "结果说明": "Result Description",
    
    # 描述性文本
    "本文档介绍了如何使用Xinference的各种镜像版本，包括Nvidia系列、MindIE系列和海光系列。": 
    "This document describes how to use various Xinference image versions, including NVIDIA, MindIE, and Hygon series.",
    
    "Xinference提供了针对不同硬件平台优化的镜像版本：":
    "Xinference provides optimized image versions for different hardware platforms:",
    
    "根据你的硬件环境选择合适的镜像：":
    "Choose the appropriate image based on your hardware environment:",
    
    "首次部署": "Initial Deployment",
    "证书管理": "Certificate Management", 
    "性能测试": "Performance Testing",
    "多机部署": "Multi-Machine Deployment",
    "链路监控": "Chain Monitoring",
    "生产部署": "Production Deployment",
    
    # 技术术语
    "推荐以下CUDA版本：": "Recommended CUDA versions:",
    "驱动版本": "Driver version",
    "CUDA版本": "CUDA version",
    "启动容器后，进入容器/opt/projects目录下，执行以下命令：": 
    "After starting the container, enter the /opt/projects directory and execute the following commands:",
    
    "Xinf服务启动完成后，即可通过访问8000端口进入Xinf WebUI界面。":
    "After the Xinf service starts successfully, you can access the Xinf WebUI interface through port 8000.",
}

def update_po_file(po_file_path):
    """更新单个po文件"""
    print(f"Processing: {po_file_path}")
    
    with open(po_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 移除fuzzy标记
    content = content.replace('#, fuzzy\n', '')
    
    # 更新翻译
    updated_count = 0
    for chinese, english in TRANSLATIONS.items():
        # 查找msgid和对应的空msgstr
        pattern = rf'msgid "{re.escape(chinese)}"\nmsgstr ""'
        replacement = f'msgid "{chinese}"\nmsgstr "{english}"'
        
        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            updated_count += 1
    
    # 保存更新后的文件
    if updated_count > 0:
        with open(po_file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Updated {updated_count} translations")
    else:
        print("  No translations updated")

def main():
    """主函数"""
    locale_dir = Path("source/locale/en/LC_MESSAGES")
    
    if not locale_dir.exists():
        print(f"Error: {locale_dir} does not exist")
        return
    
    # 查找所有po文件
    po_files = list(locale_dir.rglob("*.po"))
    
    print(f"Found {len(po_files)} .po files")
    
    for po_file in po_files:
        update_po_file(po_file)
    
    print("\nTranslation update completed!")
    print("Run 'python build_multilang.py' to rebuild the documentation.")

if __name__ == "__main__":
    main()
