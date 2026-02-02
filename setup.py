#!/usr/bin/env python3
"""
符灵 (Fú Líng) - 安装配置
"""

from setuptools import setup, find_packages

with open("README_CN.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fuling",
    version="0.1.0",
    author="deepseek-chat-v3",
    author_email="kawinkhae.101@gmail.com",
    description="符灵 (Fú Líng) - 智能命令行助手",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mai-xiyu/Fu-Ling-CLI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Shells",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=6.0",
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "black>=23.0.0",
            "flake8>=6.0.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "mypy>=1.0.0",
        ],
        "ai": [
            "openai>=1.0.0",  # 可选，用于OpenAI支持
        ],
    },
    entry_points={
        "console_scripts": [
            "fl=fuling.fuling_cli_enhanced:main",
            "fuling=fuling.fuling_cli_enhanced:main",
        ],
    },
    package_data={
        "fuling": [
            "config/themes/*.yaml",
        ],
    },
    include_package_data=True,
    project_urls={
        "Bug Reports": "https://github.com/mai-xiyu/Fu-Ling-CLI/issues",
        "Source": "https://github.com/mai-xiyu/Fu-Ling-CLI",
        "Documentation": "https://github.com/mai-xiyu/Fu-Ling-CLI/docs",
    },
)