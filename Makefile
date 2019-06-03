.PHONY: help init venv develop style-black style-pylint lint black
.DEFAULT_GOAL = help

PYTHON = python3
SHELL = bash
VENV_PATH = venv

help:
	@echo "Usage:"
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[1;34mmake %-10s\033[0m%s\n", $$1, $$2}'

init:  # Initialize git hooks for development.
	find .git/hooks -type l -exec rm {} \;
	find .githooks -type f -exec ln -sf ../../{} .git/hooks/ \;

venv:  # Create a Python virtual environment.
	@printf "Creating Python virtual environment...\n"
	rm -rf ${VENV_PATH}
	${SHELL} scripts/setup_venv.sh ${PYTHON} ${VENV_PATH}
	@printf "\n\nVirtual environment created! \033[1;34mRun \`source venv/bin/activate\` to activate it.\033[0m\n\n\n"

develop: init venv  # Set up development environment.

style-black:
	@printf "Checking code style with black...\n"
	black knead/ --check --exclude=font_pb2.py
	@printf "\033[1;34mBlack passes!\033[0m\n\n"

style-pylint:
	@printf "Checking code style with pylint...\n"
	pylint knead/ --disable=all font_pb2.py
	@printf "\033[1;34mPylint passes!\033[0m\n\n"

lint: style-black style-pylint  # Check code style with black and pylint

black:  # Format code in-place with black.
	black knead/ --exclude=font_pb2.py
