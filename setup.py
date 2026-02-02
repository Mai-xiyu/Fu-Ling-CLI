from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-cli",
    version="0.1.0",
    author="xiyu-bot-assistant",
    author_email="",
    description="An intelligent CLI assistant with AI capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/xiyu-bot-assistant/ai-cli",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "pyyaml>=6.0",
        "rich>=13.0.0",
        "prompt-toolkit>=3.0.0",
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "ollama": [
            "ollama>=0.1.0",
        ],
        "all": [
            "ollama>=0.1.0",
            "openai>=1.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "ai=ai_cli.cli:main",
            "ai-cli=ai_cli.cli:main",
        ],
    },
    include_package_data=True,
)