# Contributing Guide

Happy baking! :bread:

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

Make sure that all checks pass before committing: you should get several blue
success messages as each check passes.

Note that `knead` uses a [pre-commit git
hook](https://github.com/font-bakers/knead/blob/master/.githooks/pre-commit) to
format staged Python files in-place using `black`.

## Development details

- `knead` targets Python 3.5+ compatibility.
- `knead` uses `black` and `pylint` to format and lint code, respectively.
  - However, `black` requires Python 3.6+ to run. Thus, we test in Python 3.5
    but lint in Python 3.6. See our [Travis
    configuration](https://github.com/font-bakers/knead/blob/master/.travis.yml)
    for more details.
