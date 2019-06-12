import os
import re
from setuptools import setup, find_packages


NAME = "knead"
MAINTAINER = "The Font Bakers"
DESCRIPTION = "A command line tool for preprocessing, manipulating and serializing font files for deep learning applications."
LICENSE = "MIT"
URL = "https://github.com/font-bakers/knead/"

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
REQUIREMENTS_FILE = os.path.join(PROJECT_ROOT, "requirements.txt")
README_FILE = os.path.join(PROJECT_ROOT, "README.md")

with open(README_FILE, encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

with open(REQUIREMENTS_FILE) as f:
    INSTALL_REQUIRES = f.read().splitlines()


def get_version():
    version_file = os.path.join(NAME, "__init__.py")
    lines = open(version_file, "rt").readlines()
    version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in lines:
        mo = re.search(version_regex, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError("Unable to find version in {}.".format(version_file))


if __name__ == "__main__":
    setup(
        name=NAME,
        version=get_version(),
        maintainer=MAINTAINER,
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type="text/markdown",
        license=LICENSE,
        url=URL,
        packages=find_packages(),
        python_requires=">=3.5.2",
        install_requires=INSTALL_REQUIRES,
        entry_points={"console_scripts": ["knead = knead.__main__:main"]},
    )
