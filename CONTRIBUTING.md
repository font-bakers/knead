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
make lint
make test
```

Make sure that checks and tests pass before committing. 

Note that `knead` uses a [pre-commit git
hook](https://github.com/font-bakers/knead/blob/master/.githooks/pre-commit) to
format staged Python files in-place using `black`.
