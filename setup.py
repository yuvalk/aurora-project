#!/usr/bin/env python3
"""
Aurora Borealis Project Setup Script
"""

from setuptools import setup, find_packages

setup(
    name="aurora-borealis-toolkit",
    version="1.0.0",
    author="Aurora Enthusiast",
    description="A comprehensive toolkit for aurora borealis tracking and visualization",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Astronomy",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="aurora borealis northern lights space weather astronomy",
    entry_points={
        "console_scripts": [
            "aurora-tracker=src.aurora_tracker:main",
            "aurora-art=src.aurora_art:main",
            "aurora-graph=src.aurora_graph:main",
            "aurora-info=src.aurora_info:main",
        ],
    },
)