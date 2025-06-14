"""
セットアップスクリプト
"""

from setuptools import setup, find_packages

setup(
    name="screenshot-namer",
    version="1.0.0",
    description="macOS用スクリーンショット自動命名アプリ",
    author="Your Name",
    author_email="your.email@example.com",
    py_modules=["screenshot_namer"],
    install_requires=[
        "openai>=1.0.0",
        "watchdog>=3.0.0",
        "pillow>=10.0.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "screenshot-namer=screenshot_namer:main",
        ],
    },
    python_requires=">=3.8",
)