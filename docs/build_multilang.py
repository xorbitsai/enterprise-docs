#!/usr/bin/env python3
"""
构建多语言版本的Sphinx文档
"""

import os
import subprocess
import shutil
from pathlib import Path

def run_command(cmd, cwd=None):
    """运行命令并返回结果"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False
    print(f"Success: {result.stdout}")
    return True

def build_language(lang, output_dir):
    """构建指定语言的文档"""
    print(f"\n=== Building {lang} documentation ===")
    
    # 设置环境变量
    env = os.environ.copy()
    env['SPHINX_LANGUAGE'] = lang
    
    # 构建命令
    if lang == 'zh_CN':
        build_dir = f"build/html"
    else:
        build_dir = f"build/html/{lang}"
    
    cmd = f"sphinx-build -b html -D language={lang} source {build_dir}"
    
    result = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error building {lang}: {result.stderr}")
        return False
    
    print(f"Successfully built {lang} documentation")
    return True

def update_switcher_config():
    """更新语言切换器配置"""
    switcher_config = [
        {
            "name": "简体中文(Chinese)",
            "version": "zh_CN",
            "url": "/",
            "preferred": True
        },
        {
            "name": "English",
            "version": "en", 
            "url": "/en/"
        }
    ]
    
    import json
    
    # 为中文版本创建switcher.json
    zh_switcher_path = Path("build/html/_static/switcher.json")
    zh_switcher_path.parent.mkdir(parents=True, exist_ok=True)
    with open(zh_switcher_path, 'w', encoding='utf-8') as f:
        json.dump(switcher_config, f, ensure_ascii=False, indent=2)
    
    # 为英文版本创建switcher.json
    en_switcher_path = Path("build/html/en/_static/switcher.json")
    en_switcher_path.parent.mkdir(parents=True, exist_ok=True)
    with open(en_switcher_path, 'w', encoding='utf-8') as f:
        json.dump(switcher_config, f, ensure_ascii=False, indent=2)

def main():
    """主函数"""
    print("Building multilingual Xinference documentation...")
    
    # 确保在正确的目录
    os.chdir(Path(__file__).parent)
    
    # 生成翻译模板
    print("\n=== Generating translation templates ===")
    if not run_command("sphinx-build -b gettext source build/locale"):
        return False
    
    # 更新翻译文件
    print("\n=== Updating translation files ===")
    run_command("sphinx-intl update -p build/locale -l zh_CN")
    run_command("sphinx-intl update -p build/locale -l en")
    
    # 构建中文版本（默认）
    if not build_language('zh_CN', 'build/html'):
        return False
    
    # 构建英文版本
    if not build_language('en', 'build/html/en'):
        return False
    
    # 更新语言切换器配置
    print("\n=== Updating language switcher ===")
    update_switcher_config()
    
    print("\n=== Build completed successfully! ===")
    print("Chinese version: build/html/")
    print("English version: build/html/en/")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
