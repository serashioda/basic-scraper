"""Setup for scraper."""

from setuptools import setup

setup(
    name="scraper",
    description="This module demonstrates web scraping and beautiful soup",
    version=1.1,
    author="Sera",
    author_email="",
    license="MIT",
    package_dir={'': 'src'},
    py_modules=["scraper.py"],
    install_requires=["beautifulsoup"],
    extras_require={"test": ["pytest", "pytest-watch", "pytest-cov", "tox"]},
    entry_points={}
)
