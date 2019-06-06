#/bin/bash
# Sets up Python virtual environment for development.
set -e

PYTHON=$1
VENV_PATH=$2
REQUIREMENTS_FILE=$3

$PYTHON -m venv $VENV_PATH
source $VENV_PATH/bin/activate
pip install --upgrade pip

grep -v \# $REQUIREMENTS_FILE | while read line
do
   echo $line
   pip install $line
done

pip install -e .

deactivate
