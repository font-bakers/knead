.PHONY: help init venv format
.DEFAULT_GOAL = help

PYTHON = python
SHELL = bash
VENV_PATH = venv

help:
	@echo "Usage:"
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[1;34mmake %-10s\033[0m%s\n", $$1, $$2}'

init:  # Initialize git hooks for development.
	find .git/hooks -type l -exec rm {} \;
	find .githooks -type f -exec ln -sf ../../{} .git/hooks/ \;

venv:  # Create a Python virtual environment.
	rm -rf ${VENV_PATH}
	${SHELL} scripts/setup_venv.sh ${PYTHON} ${VENV_PATH}

format:  # Format code in-place with black.
	black knead/ --exclude=font_pb2.py
