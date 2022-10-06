import ast
import io
import re
import sys

from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

_description_re = re.compile(r"description\s+=\s+(?P<description>.*)")

with open("lektor_jinja_content.py", "rb") as f:
    description = str(
        ast.literal_eval(_description_re.search(f.read().decode("utf-8")).group(1))
    )

dev_require = [
    "flake8",
    "ipdb",
    "ipython",
    "pytest",
    "pytest-cov",
    "pytest-mock",
    "pytest-click",
    "pytest-pylint",
    # installed for testing. See https://github.com/terminal-labs/lektor-jinja-content/issues/15
    "lektor",
]

setup(
    author="Terminal Labs, Joseph Nix",
    author_email="solutions@terminallabs.com",
    description=description,
    extras_require={"dev": dev_require},
    keywords="Lektor plugin static-site jinja jinja2",
    license="BSD-3-Clause",
    long_description=readme,
    long_description_content_type="text/markdown",
    name="lektor-jinja-content",
    py_modules=["lektor_jinja_content"],
    tests_require=dev_require,
    url="https://github.com/terminal-labs/lektor-jinja-content",
    version="0.4.4",
    classifiers=[
        "Environment :: Plugins",
        "Environment :: Web Environment",
        "Framework :: Lektor",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points={
        "lektor.plugins": ["jinja-content = lektor_jinja_content:JinjaContentPlugin"]
    },
)
