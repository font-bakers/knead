import os
import re
from setuptools import setup, find_packages


NAME = "knead"
MAINTAINER = "The Font Bakers"
DESCRIPTION = "A command line tool for preprocessing, manipulating and serializing font files for deep learning applications."
LICENSE = "MIT"
URL = "https://github.com/font-bakers/knead"
PROJECT_URLS = {
    "Issue Tracker": "https://github.com/font-bakers/knead/issues",
    "Documentation": "https://font-bakers.github.io/knead/",
}
PYTHON_REQUIRES = ">=3.5.2"

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
REQUIREMENTS_FILE = os.path.join(PROJECT_ROOT, "requirements.txt")
README_FILE = os.path.join(PROJECT_ROOT, "README.md")

try:
    with open(README_FILE, encoding="utf-8") as f:
        LONG_DESCRIPTION = "\n" + f.read()
        LONG_DESCRIPTION_CONTENT_TYPE = "text/markdown"
except FileNotFoundError:
    LONG_DESCRIPTION = DESCRIPTION
    LONG_DESCRIPTION_CONTENT_TYPE = "text/plain"

with open(REQUIREMENTS_FILE) as f:
    INSTALL_REQUIRES = f.read().splitlines()

CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
    "Environment :: Console",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.5",
    "Topic :: Scientific/Engineering",
    "Topic :: Text Processing :: Fonts",
]


def get_version():
    version_file = os.path.join(NAME, "__init__.py")
    lines = open(version_file, "rt").readlines()
    version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in lines:
        matches = re.search(version_regex, line, re.M)
        if matches:
            return matches.group(1)
    raise RuntimeError("Unable to find version in {}.".format(version_file))


if __name__ == "__main__":
    setup(
        name=NAME,
        version=get_version(),
        maintainer=MAINTAINER,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
        license=LICENSE,
        classifiers=CLASSIFIERS,
        url=URL,
        project_urls=PROJECT_URLS,
        packages=find_packages(),
        python_requires=PYTHON_REQUIRES,
        install_requires=INSTALL_REQUIRES,
        entry_points={"console_scripts": ["knead = knead.__main__:main"]},
    )
