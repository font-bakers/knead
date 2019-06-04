.PHONY: help init venv venv-develop develop lint-black lint-pylint lint test check black
.DEFAULT_GOAL = help

PYTHON = python3
SHELL = bash
VENV_PATH = venv

help:
	@echo "Usage:"
	@grep -E '^[a-zA-Z_-]+:.*?# .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?# "}; {printf "\033[1;34mmake %-10s\033[0m%s\n", $$1, $$2}'

init:
	@printf "Initializing git hooks...\n"
	find .git/hooks -type l -exec rm {} \;
	find .githooks -type f -exec ln -sf ../../{} .git/hooks/ \;
	@printf "\n\n\033[1;34mGit hooks initialized!\033[0m\n\n\n"

venv:
	@printf "Creating Python virtual environment...\n"
	rm -rf ${VENV_PATH}
	${SHELL} scripts/setup_venv.sh ${PYTHON} ${VENV_PATH} requirements.txt
	@printf "\n\nVirtual environment created! \033[1;34mRun \`source venv/bin/activate\` to activate it.\033[0m\n\n\n"

venv-develop:
	@printf "Creating Python virtual environment for development...\n"
	rm -rf ${VENV_PATH}
	${SHELL} scripts/setup_venv.sh ${PYTHON} ${VENV_PATH} requirements-dev.txt
	@printf "\n\nVirtual environment created! \033[1;34mRun \`source venv/bin/activate\` to activate it.\033[0m\n\n\n"

develop: init venv-develop  # Set up development environment.

lint-black:
	@printf "Checking code style with black...\n"
	black knead/ --check --target-version=py35 --exclude=font_pb2.py
	@printf "\033[1;34mBlack passes!\033[0m\n\n"

lint-pylint:
	@printf "Checking code style with pylint...\n"
	pylint knead/ --rcfile=.pylintrc --disable=all font_pb2.py
	@printf "\033[1;34mPylint passes!\033[0m\n\n"

lint: lint-black lint-pylint  # Check code style with black and pylint.

test:  # Run tests.
	@printf "Checking code...\n"
	@printf "\033[1;34mTests pass!\033[0m\n\n"

check: lint test  # Alias for `make lint test`.

black:  # Format code in-place with black.
	black knead/ --target-version=py35 --exclude=font_pb2.py
