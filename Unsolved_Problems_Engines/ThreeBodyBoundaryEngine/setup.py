"""
ThreeBodyBoundaryEngine - Setup Script

Author: GNJz (Qquarts)
Version: 1.2.1
"""

from setuptools import setup, find_packages
import os

# Single Source of Truth: 버전은 __init__.py에서 가져옴
def get_version():
    """__init__.py에서 버전을 읽어옴"""
    version_file = os.path.join(os.path.dirname(__file__), "src", "three_body_boundary_engine", "__init__.py")
    with open(version_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    return "1.2.1"  # fallback

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="three-body-boundary-engine",
    version=get_version(),
    author="GNJz (Qquarts)",
    # author_email 제거 (가짜 이메일 방지)
    description="Three-Body Problem Boundary Convergence Analysis Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qquartsco-svg/BDS_Engine",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": ["pytest", "pytest-cov"],
    },
)

