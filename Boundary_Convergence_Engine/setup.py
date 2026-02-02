"""
Setup script for Boundary Convergence Engine
Boundary Convergence Engine 설치 스크립트

산업용/상업용/연구용 독립 모듈
Industrial/Commercial/Research Standalone Module

⚠️ 중요 명확화:
- 이 엔진은 π를 계산하는 것이 아니라,
- 경계-공간 정합의 동역학적 과정을 구현합니다.

Author: GNJz (Qquarts)
License: MIT
Version: 1.0.0
"""

from setuptools import setup, find_packages
from pathlib import Path

# README 읽기
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="boundary-convergence-engine",
    version="1.0.0",
    author="GNJz (Qquarts)",
    author_email="",  # 필요시 추가
    description="Boundary Convergence Engine - 경계-공간 정합 계수 (Boundary-Space Alignment Coefficient)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gnjz/boundary-convergence-engine",  # 필요시 업데이트
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Healthcare Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[],  # 표준 라이브러리만 사용 (Standard library only)
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    keywords=[
        "boundary convergence",
        "space filling",
        "cognitive modeling",
        "geometric modeling",
        "mathematical modeling",
        "boundary-space alignment",
    ],
    project_urls={
        "Documentation": "https://github.com/gnjz/boundary-convergence-engine",
        "Source": "https://github.com/gnjz/boundary-convergence-engine",
        "Tracker": "https://github.com/gnjz/boundary-convergence-engine/issues",
    },
)

