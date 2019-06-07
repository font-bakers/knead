import os
import re
from setuptools import setup, find_packages


NAME = "knead"
AUTHOR = "The Font Bakers"
DESCRIPTION = "A data processing library for fonts and typefaces, targeting deep learning applications."
URL = "https://github.com/font-bakers/knead/"
LICENSE = "MIT"


def get_version():
    version_file = os.path.join(NAME, "__init__.py")
    lines = open(version_file, "rt").readlines()
    version_regex = r"^__version__ = ['\"]([^'\"]*)['\"]"
    for line in lines:
        mo = re.search(version_regex, line, re.M)
        if mo:
            return mo.group(1)
    raise RuntimeError("Unable to find version in %s." % (version_file,))


if __name__ == "__main__":
    setup(
        name=NAME,
        version=get_version(),
        maintainer=AUTHOR,
        description=DESCRIPTION,
        license=LICENSE,
        url=URL,
        packages=find_packages(),
        python_requires=">=3.5.2",
        entry_points={"console_scripts": ["knead = knead.__main__:main"]},
    )
