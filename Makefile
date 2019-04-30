.PHONY: help venv format
.DEFAULT_GOAL = help

PYTHON = python
SHELL = bash
VENV_PATH = venv

help:
	@echo "Usage:"
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[1;34mmake %-10s\033[0m%s\n", $$1, $$2}'

venv:  # Create a Python virtual environment.
	rm -rf ${VENV_PATH}
	${SHELL} scripts/setup_venv.sh ${PYTHON} ${VENV_PATH}

format:  # Format code in-place with black.
	black src/
