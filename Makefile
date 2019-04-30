.PHONY: venv format

PYTHON = python
SHELL = bash
VENV_PATH = venv

venv:  # Create a Python virtual environment.
	rm -rf ${VENV_PATH}
	${SHELL} scripts/setup_venv.sh ${PYTHON} ${VENV_PATH}

format:  # Format code in-place with black.
	black src/
