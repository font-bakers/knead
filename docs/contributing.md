# Contributing Guide

[![GitHub Issues](https://img.shields.io/github/issues/font-bakers/knead.svg)](https://github.com/font-bakers/knead/issues)
[![GitHub Pull Requests](https://img.shields.io/github/issues-pr/font-bakers/knead.svg)](https://github.com/font-bakers/knead/pulls)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

Happy baking!

## Set up development environment

```bash
git clone https://github.com/font-bakers/knead.git
cd knead/
make develop
source venv/bin/activate
# Do your work...
deactivate
```

## Before committing

```bash
make check
```

This will both lint the `knead/` directory (with `black` and `pylint`), and run
test scripts. You may lint and test separately with `make lint` and `make test`,
respectively.

Make sure that all checks pass before committing: you should get several blue
success messages as each check passes.

Note that `knead` uses a [pre-commit git
hook](https://github.com/font-bakers/knead/blob/master/.githooks/pre-commit) to
format staged Python files in-place using `black`.

## Development details

- `knead` follows the [Semantic Versioning
  2.0.0](https://semver.org/#semantic-versioning-200) specification.
- `knead` targets Python 3.5+ (specifically, 3.5.2+) compatibility.
- `knead` uses `black` and `pylint` to format and lint code, respectively.
  - However, `black` requires Python 3.6+ to run. Thus, we test in Python 3.5
    but lint in Python 3.6. See our [Travis
    configuration](https://github.com/font-bakers/knead/blob/master/.travis.yml)
    for more details.
- `knead` contains integration tests in the form of the [`test.sh`
  script](https://github.com/font-bakers/knead/blob/master/scripts/test.sh).
  `knead` is currently not unit tested.

